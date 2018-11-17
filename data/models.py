from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel
from datetime import datetime
import pytz
from enum import Enum

BCF_URL_BASE = "https://www.bcferries.com/current_conditions"

class DayOfWeek(Enum):
    MON = "Monday"
    TUE = "Tuesday"
    WED = "Wednesday"
    THU = "Thursday"
    FRI = "Friday"
    SAT = "Saturday"
    SUN = "Sunday"


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
    actual_departure = models.DateTimeField(null=True, blank=True)
    eta_or_arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.DO_NOTHING)
    departed = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    percent_full = models.IntegerField(default=None, null=True, blank=True)
    day_of_week = models.CharField(max_length=3, choices=[
        (tag, tag.value) for tag in DayOfWeek
    ], null=True, blank=True)

    @property
    def scheduled_departure_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.scheduled_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def actual_departure_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.actual_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def eta_or_arrival_time_local(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.eta_or_arrival_time.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

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

        super(Sailing, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return "{} @ {}".format(self.route, self.scheduled_departure_local)


class SailingEvent(PolymorphicModel):
    sailing = models.ForeignKey(Sailing, null=False, blank=False, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def time(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


class RouteEvent(PolymorphicModel):
    route = models.ForeignKey(Route, null=False, blank=False, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def time(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


class DepartureTimeEvent(SailingEvent):
    old_departure = models.DateTimeField(null=True, blank=True)
    new_departure = models.DateTimeField(null=True, blank=True)

    @property
    def departure(self) -> str:
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.new_departure.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

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

    def __repr__(self) -> str:
        return "<ArrivalTimeEvent: [{}] {}{}>".format(
            self.time,
            "ETA " if self.is_eta else "",
            self.arrival
        )

class DepartedEvent(SailingEvent):
    def __repr__(self) -> str:
        return "<DepartedEvent: [{}]>".format(
            self.time
        )


class ArrivedEvent(SailingEvent):
    def __repr__(self) -> str:
        return "<ArrivedEvent: [{}]>".format(
            self.time
        )


class StatusEvent(SailingEvent):
    old_status = models.ForeignKey(Status, null=True, blank=True, related_name="old_status", on_delete=models.DO_NOTHING)
    new_status = models.ForeignKey(Status, null=True, blank=True, related_name="new_status", on_delete=models.DO_NOTHING)

    def __repr__(self) -> str:
        return "<StatusEvent: [{}] {}>".format(
            self.time, self.new_status
        )


class FerryEvent(SailingEvent):
    old_ferry = models.ForeignKey(Ferry, null=True, blank=True, related_name="old_ferry", on_delete=models.DO_NOTHING)
    new_ferry = models.ForeignKey(Ferry, null=True, blank=True, related_name="new_ferry", on_delete=models.DO_NOTHING)

    def __repr__(self) -> str:
        return "<FerryEvent: [{}] {}>".format(
            self.time, self.new_ferry
        )


class PercentFullEvent(SailingEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return "<PercentFullEvent: [{}] {}%>".format(
            self.time, self.new_value
        )


class CarWaitEvent(RouteEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return "<CarWaitEvent: [{}] {}%>".format(
            self.time, self.new_value
        )


class OversizeWaitEvent(RouteEvent):
    old_value = models.IntegerField(null=True, blank=True)
    new_value = models.IntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return "<OversizeWaitEvent:[{}] {}%>".format(
            self.time, self.new_value
        )
