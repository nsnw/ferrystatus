from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel
import pytz


class Run(PolymorphicModel):
    timestamp = models.DateTimeField(auto_now=True)
    successful = models.BooleanField(default=False)
    status = models.CharField(max_length=256, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    @property
    def local_timestamp(self):
        tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)
        return self.timestamp.astimezone(tz)

    @property
    def to_date_time(self) -> str:
        return self.local_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def html(self) -> list:
        return self.rawhtml_set.all()

    def set_status(self, status, successful: bool = False):
        self.status = status
        self.successful = successful
        self.save()

    def __repr__(self) -> str:
        return "<{}: {}>".format(
            self.__class__.__name__,
            self.to_date_time
        )


class ConditionsRun(Run):
    pass


class DeparturesRun(Run):
    pass


class LocationsRun(Run):
    pass


class SailingDetailRun(Run):
    pass


class RawHTML(PolymorphicModel):
    run = models.ForeignKey(Run, null=False, blank=False, on_delete=models.CASCADE)
    data = models.TextField(null=True, blank=True)


class ConditionsRawHTML(RawHTML):
    pass


class DeparturesRawHTML(RawHTML):
    pass


class LocationsRawHTML(RawHTML):
    url = models.CharField(max_length=256, null=False, blank=False)
