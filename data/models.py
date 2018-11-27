from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel
from datetime import datetime, timedelta
import pytz
from enum import Enum
import logging

logger = logging.getLogger(__name__)

BCF_URL_BASE = "https://www.bcferries.com/current_conditions"

class DayOfWeek(Enum):
    MON = "Monday"
    TUE = "Tuesday"
    WED = "Wednesday"
    THU = "Thursday"
    FRI = "Friday"
    SAT = "Saturday"
    SUN = "Sunday"


class FerryStatus(Enum):
    IN_PORT = "In Port"
    UNDER_WAY = "Under Way"
    OFFLINE = "Offline"


class Terminal(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    short_name = models.CharField(max_length=16, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Terminal: {} ({})>".format(self.name, self.short_name)


class Destination(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    terminal = models.ForeignKey(Terminal, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    source = models.ForeignKey(Terminal, null=False, blank=False,
                               on_delete=models.DO_NOTHING)
    destination = models.ForeignKey(Destination, null=False, blank=False,
                                    on_delete=models.DO_NOTHING)
    route_code = models.IntegerField(null=False, blank=False)
    car_waits = models.IntegerField(default=None, null=True, blank=True)
    oversize_waits = models.IntegerField(default=None, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    @property
    def url(self) -> str:
        return "{}/arrivals-departures.html?dept={}&route={}".format(
            BCF_URL_BASE,
            self.source.short_name,
            self.route_code
        )

    @property
    def next_sailing(self) -> "Sailing":
        sailing = Sailing.objects.filter(
            route=self,
            scheduled_departure__gt=datetime.now(pytz.UTC)
        ).order_by('scheduled_departure').first()

        return sailing

    @property
    def as_dict(self) -> dict:
        response = {
            "id": self.pk,
            "name": self.name,
            "source": self.source.name,
            "destination": self.destination.name,
            "car_waits": self.car_waits,
            "oversize_waits": self.oversize_waits,
            "next_sailing": self.next_sailing.as_dict,
            "duration": self.duration
        }

        return response

    def __str__(self) -> str:
        return "{} -> {} ({})".format(
            self.source, self.destination, self.route_code
        )

    def __repr__(self) -> str:
        return "<Route: {} -> {} ({})>".format(
            self.source, self.destination, self.route_code
        )


class Ferry(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    destination = models.ForeignKey(Destination, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=32, choices=[
        (tag, tag.value) for tag in FerryStatus
    ], null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    heading = models.CharField(max_length=8, null=True, blank=True)

    @property
    def current_sailing(self) -> "Sailing":
        try:
            return self.sailing_set.get(departed=True, arrived=False)
        except:
            return None

    @property
    def next_sailing(self) -> "Sailing":
        try:
            return self.sailing_set.filter(departed=False).\
                order_by("scheduled_departure").\
                first()
        except:
            return None

    @property
    def as_dict(self) -> dict:
        response = {
            "name": self.name,
            "status": self.status,
            "last_updated": self.last_updated
        }

        if self.destination:
            response['destination'] = self.destination.name

        if self.heading:
            response['heading'] = self.heading

        return response

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Ferry: {}>".format(self.name)


class Status(models.Model):
    status = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self) -> str:
        return self.status if self.status else "N/A"

    def __repr__(self) -> str:
        return "<Status: {}>".format(str(self))


class Sailing(models.Model):
    route = models.ForeignKey(Route, null=False, blank=False, on_delete=models.DO_NOTHING)
    ferry = models.ForeignKey(Ferry, null=True, blank=True, on_delete=models.DO_NOTHING)
    scheduled_departure = models.DateTimeField(null=False, blank=False)
    scheduled_arrival = models.DateTimeField(null=True, blank=True)
    actual_departure = models.DateTimeField(null=True, blank=True)
    eta_or_arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.DO_NOTHING)
    departed = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    percent_full = models.IntegerField(default=None, null=True, blank=True)
    sailing_time = models.CharField(max_length=8, null=True, blank=True)
    day_of_week = models.CharField(max_length=16, choices=[
        (tag, tag.value) for tag in DayOfWeek
    ], null=True, blank=True)
    late_leaving = models.IntegerField(null=True, blank=True)
    late_arriving = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    @property
    def scheduled_departure_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.scheduled_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def scheduled_arrival_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.scheduled_arrival.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def actual_departure_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.actual_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def eta_or_arrival_time_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.eta_or_arrival_time.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def scheduled_departure_hour_minute(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.scheduled_departure.astimezone(tz).strftime("%-I:%M%p").lower()

    @property
    def scheduled_arrival_hour_minute(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.scheduled_arrival.astimezone(tz).strftime("%-I:%M%p").lower()

    @property
    def actual_departure_hour_minute(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.actual_departure.astimezone(tz).strftime("%-I:%M%p").lower()

    @property
    def eta_or_arrival_time_hour_minute(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.eta_or_arrival_time.astimezone(tz).strftime("%-I:%M%p").lower()

    @property
    def as_dict(self) -> dict:
        response = {
            "id": self.pk,
            "route": self.route.name,
            "route_id": self.route.id,
            "scheduled_departure": self.scheduled_departure_local,
            "scheduled_departure_hour_minute": self.scheduled_departure_hour_minute,
            "state": self.state
        }

        if self.ferry:
            response['ferry'] = self.ferry.name

        if self.actual_departure:
            response['actual_departure'] = self.actual_departure_local
            response['actual_departure_hour_minute'] = self.actual_departure_hour_minute

        if self.eta_or_arrival_time:
            response['eta_or_arrival_time'] = self.eta_or_arrival_time_local
            response['eta_or_arrival_time_hour_minute'] = self.eta_or_arrival_time_hour_minute

        if self.scheduled_arrival:
            response['scheduled_arrival'] = self.scheduled_arrival
            response['scheduled_arrival_hour_minute'] = self.scheduled_arrival_hour_minute

        if self.status:
            response['status'] = self.status.status

        if self.percent_full:
            response['percent_full'] = self.percent_full

        if self.duration:
            response['duration'] = self.duration

        if self.late_leaving:
            response['late_leaving'] = self.late_leaving

        if self.late_arriving:
            response['late_arriving'] = self.late_arriving

        response['events'] = [
            event.as_dict for event in self.sailingevent_set.all().order_by('timestamp')
        ]

        return response

    @property
    def state(self) -> str:
        if self.departed:
            if self.arrived:
                return "Arrived"
            else:
                return "Departed"
        else:
            return "Not departed"



    @property
    def info(self) -> str:
        info = "{}: {}".format(str(self), self.state)

        if self.ferry:
            info += " Ferry: {}".format(self.ferry)

        if self.actual_departure:
            info += " Departed at: {}".format(self.actual_departure_local)

        if self.eta_or_arrival_time:
            if self.arrived:
                info += " Arrived at: {}".format(self.eta_or_arrival_time_local)
            else:
                info += " ETA: {}".format(self.eta_or_arrival_time_local)

        if self.percent_full:
            info += " - {}% full".format(self.percent_full)

        return info

    def save(self, *args, **kwargs):
        if not self.day_of_week:
            tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
            day_of_week = self.scheduled_departure.astimezone(tz).strftime("%A")
            self.day_of_week = day_of_week

        if not self.sailing_time:
            tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
            self.sailing_time = self.scheduled_departure.astimezone(tz).strftime("%H:%M")

        if not self.duration and self.arrived is True:
            td = self.eta_or_arrival_time - self.actual_departure
            self.duration = td.seconds / 60
            logger.debug("Sailing duration was {}".format(self.duration))

        if not self.scheduled_arrival:
            self.scheduled_arrival = self.scheduled_departure + timedelta(minutes=self.route.duration)
            logger.debug("Set scheduled arrival to {}".format(self.scheduled_arrival_hour_minute))

        if not self.late_leaving and self.departed is True:
            if self.actual_departure < self.scheduled_departure:
                logger.debug("Sailing left early")
                td = self.scheduled_departure - self.actual_departure
                early = True
            else:
                td = self.actual_departure - self.scheduled_departure
                early = False

            difference = td.seconds / 60

            if early:
                self.late_leaving = -difference
            else:
                self.late_leaving = difference

            logger.debug("Sailing scheduled: {}, left at {}".format(
                self.scheduled_departure_hour_minute, self.actual_departure_hour_minute
            ))
            logger.debug("Sailing was {} mins {} leaving".format(
                difference,
                "early" if early else "late"
            ))

        if not self.late_arriving and self.arrived is True:
            if self.eta_or_arrival_time < self.scheduled_arrival:
                logger.debug("Sailing arrived early")
                td = self.scheduled_arrival - self.eta_or_arrival_time
                early = True
            else:
                td = self.eta_or_arrival_time - self.scheduled_arrival
                early = False

            difference = td.seconds / 60

            if early:
                self.late_arriving = -difference
            else:
                self.late_arriving = difference

            logger.debug("Sailing scheduled: {}, arrived at {}".format(
                self.scheduled_arrival_hour_minute, self.eta_or_arrival_time_hour_minute
            ))
            logger.debug("Sailing was {} mins {} arriving".format(
                difference,
                "early" if early else "late"
            ))

        super(Sailing, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return "{} @ {}".format(self.route, self.scheduled_departure_local)


class SailingEvent(PolymorphicModel):
    sailing = models.ForeignKey(Sailing, null=False, blank=False, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def time(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz).strftime("%H:%M")

    @property
    def as_dict(self) -> str:
        return {
            "timestamp": self.timestamp,
            "local_time": self.time,
            "text": self.text
        }


class RouteEvent(PolymorphicModel):
    route = models.ForeignKey(Route, null=False, blank=False, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def time(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


class LocationEvent(PolymorphicModel):
    ferry = models.ForeignKey(Ferry, null=False, blank=False, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def time(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def updated(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.last_updated.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


class DepartureTimeEvent(SailingEvent):
    old_departure = models.DateTimeField(null=True, blank=True)
    new_departure = models.DateTimeField(null=True, blank=True)

    @property
    def departure(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.new_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def text(self) -> str:
        return "Departure time changed to {}".format(
            self.departure
        )

    def __repr__(self) -> str:
        return "<DepartureTimeEvent: [{}] {}>".format(
            self.time, self.departure
        )


class ArrivalTimeEvent(SailingEvent):
    old_arrival = models.DateTimeField(null=True, blank=True)
    new_arrival = models.DateTimeField(null=True, blank=True)
    is_eta = models.BooleanField(default=False)

    @property
    def arrival(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.new_arrival.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def text(self) -> str:
        if self.is_eta:
            return "ETA changed to {}".format(
                self.arrival
            )
        else:
            return "Arrival time changed to {}".format(
                self.arrival
            )

    def __repr__(self) -> str:
        return "<ArrivalTimeEvent: [{}] {}{}>".format(
            self.time,
            "ETA " if self.is_eta else "",
            self.arrival
        )

class DepartedEvent(SailingEvent):
    @property
    def text(self) -> str:
        return "Sailing has departed"

    def __repr__(self) -> str:
        return "<DepartedEvent: [{}]>".format(
            self.time
        )


class ArrivedEvent(SailingEvent):
    @property
    def text(self) -> str:
        return "Sailing has arrived"

    def __repr__(self) -> str:
        return "<ArrivedEvent: [{}]>".format(
            self.time
        )


class StatusEvent(SailingEvent):
    old_status = models.ForeignKey(Status, null=True, blank=True, related_name="old_status", on_delete=models.DO_NOTHING)
    new_status = models.ForeignKey(Status, null=True, blank=True, related_name="new_status", on_delete=models.DO_NOTHING)

    @property
    def text(self) -> str:
        return "Status changed to {}".format(self.new_status)

    def __repr__(self) -> str:
        return "<StatusEvent: [{}] {}>".format(
            self.time, self.new_status
        )


class FerryEvent(SailingEvent):
    old_ferry = models.ForeignKey(Ferry, null=True, blank=True, related_name="old_ferry", on_delete=models.DO_NOTHING)
    new_ferry = models.ForeignKey(Ferry, null=True, blank=True, related_name="new_ferry", on_delete=models.DO_NOTHING)

    @property
    def text(self) -> str:
        return "Ferry changed to {}".format(self.new_ferry.name)

    def __repr__(self) -> str:
        return "<FerryEvent: [{}] {}>".format(
            self.time, self.new_ferry
        )


class PercentFullEvent(SailingEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    @property
    def text(self) -> str:
        return "Sailing now {}% full".format(self.new_value)

    def __repr__(self) -> str:
        return "<PercentFullEvent: [{}] {}%>".format(
            self.time, self.new_value
        )


class CarWaitEvent(RouteEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return "<CarWaitEvent: [{}] {}>".format(
            self.time, self.new_value
        )


class OversizeWaitEvent(RouteEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return "<OversizeWaitEvent:[{}] {}>".format(
            self.time, self.new_value
        )


class InPortEvent(LocationEvent):
    def __repr__(self) -> str:
        return "<InPortEvent: [{}]>".format(
            self.last_updated
        )


class UnderWayEvent(LocationEvent):
    def __repr__(self) -> str:
        return "<UnderWayEvent: [{}]>".format(
            self.last_updated
        )


class OfflineEvent(LocationEvent):
    def __repr__(self) -> str:
        return "<OfflineEvent: [{}]>".format(
            self.last_updated
        )


class StoppedEvent(LocationEvent):
    def __repr__(self) -> str:
        return "<StoppedEvent: [{}]>".format(
            self.last_updated
        )


class HeadingEvent(LocationEvent):
    old_value = models.CharField(max_length=8, null=True, blank=True)
    new_value = models.CharField(max_length=8, null=True, blank=True)

    def __repr__(self) -> str:
        return "<HeadingEvent: [{}]>".format(
            self.last_updated
        )


class DestinationEvent(LocationEvent):
    destination = models.ForeignKey(Destination, null=True, blank=True, on_delete=models.DO_NOTHING)
    def __repr__(self) -> str:
        return "<DestinationEvent: [{}]>".format(
            self.last_updated
        )
