import logging
from . import response
from data.models import Route

logger = logging.getLogger(__name__)

def get_all(request):
    routes = [
        route.as_dict for route in Route.objects.all().order_by('route_code')
    ]

    return response(request, routes)


