import logging
from pytz import timezone
from django.db.models import Q
from . import response, error
from data.models import Sailing, Route
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_all(request):
    tz = timezone('UTC')
    now = tz.localize(datetime.now())
    hour_ago = now - timedelta(hours=1)
    sailings = [
        sailing.as_dict for sailing in Sailing.objects.filter(
            Q(scheduled_departure__gt=now)|Q(eta_or_arrival_time__gt=hour_ago)
        ).order_by('scheduled_departure')
    ]

    return response(request, sailings)


def get_really_all(request):
    tz = timezone('UTC')
    now = tz.localize(datetime.now())
    sailings = [
        sailing.as_dict for sailing in Sailing.objects.filter(
            Q(status__status="Cancelled")|Q(eta_or_arrival_time__gt=now)
        )
    ]

    return response(request, sailings)


def get_sailing(request, sailing: int):
    try:
        sailing = Sailing.objects.get(pk=sailing)
    except Sailing.DoesNotExist:
        return error(
            request,
            404,
            "Unknown sailing"
        )

    return response(request, sailing.as_dict)


def get_sailing_by_route(request, source: str, destination: str = None):
    tz = timezone('UTC')
    now = tz.localize(datetime.now())
    hour_ago = now - timedelta(hours=1)

    try:
        logger.debug("Querying for sailings with source {}...".format(source.upper()))
        sailings = Sailing.objects.filter(
            route__source__short_name=source.upper()
        )

        if destination:
            logger.debug("Querying for sailings with destination {}...".format(destination.upper()))
            sailings = sailings.filter(
                route__destination__terminal__short_name=destination.upper()
            )

        sailings = [
            s.as_dict for s in sailings.filter(
                Q(scheduled_departure__gt=now)|Q(eta_or_arrival_time__gt=hour_ago)
            ).order_by('scheduled_departure')
        ]
    except Route.DoesNotExist:
        return error(
            request,
            404,
            "Unknown route"
        )

    return response(request, sailings)


def get_sailing_by_route_id(request, route_id: int):
    tz = timezone('UTC')
    now = tz.localize(datetime.now())
    hour_ago = now - timedelta(hours=1)

    try:
        logger.debug("Querying for sailings with route ID {}...".format(
            route_id
        ))
        route = Route.objects.get(id=route_id)
        sailings = [
            s.as_dict for s in Sailing.objects.filter(
                route__id=route_id
            ).filter(
                Q(scheduled_departure__gt=hour_ago)|Q(eta_or_arrival_time__gt=hour_ago)
            ).order_by('scheduled_departure')
        ]
        data = {
            "route": route.as_dict,
            "sailings": sailings
        }
    except Route.DoesNotExist:
        return error(
            request,
            404,
            "Unknown route"
        )

    return response(request, data)
