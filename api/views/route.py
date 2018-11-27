import logging
from pytz import timezone
from django.db.models import Q
from . import response, error
from data.models import Route
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_all(request):
    #tz = timezone('UTC')
    #now = tz.localize(datetime.now())
    #hour_ago = now - timedelta(hours=1)
    routes = [
        route.as_dict for route in Route.objects.all()
    ]

    return response(request, routes)


