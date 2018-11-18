from django.contrib import admin
from .models import (Terminal, Route, Ferry, Sailing, Destination, Status,
                     SailingEvent, ArrivalTimeEvent, ArrivedEvent, StatusEvent,
                     FerryEvent, DepartureTimeEvent, DepartedEvent,
                     PercentFullEvent, CarWaitEvent, OversizeWaitEvent)

admin.site.register(Terminal)
admin.site.register(Route)
admin.site.register(Ferry)
admin.site.register(Sailing)
admin.site.register(Destination)
admin.site.register(Status)
admin.site.register(SailingEvent)
admin.site.register(ArrivalTimeEvent)
admin.site.register(ArrivedEvent)
admin.site.register(StatusEvent)
admin.site.register(FerryEvent)
admin.site.register(DepartureTimeEvent)
admin.site.register(DepartedEvent)
admin.site.register(PercentFullEvent)
admin.site.register(CarWaitEvent)
admin.site.register(OversizeWaitEvent)

# Register your models here.
