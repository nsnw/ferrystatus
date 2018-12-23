from django.urls import path
from .views import ping, ferry, sailing, route, terminal

urlpatterns = [
    path('ping', ping, name="ping"),
    path('ferries', ferry.get_all, name="get_all_ferries"),
    path('sailings', sailing.get_all, name="get_all_sailings"),
    path('all-sailings', sailing.get_really_all, name="get_really_all_sailings"),
    path('sailings/route/<int:route_id>', sailing.get_sailing_by_route_id, name="get_sailing_by_route_id"),
    path('sailings/<int:sailing>', sailing.get_sailing, name="get_sailing"),
    path('sailings/<str:source>', sailing.get_sailing_by_route, name="get_sailing_from"),
    path('sailings/<str:source>/<str:destination>', sailing.get_sailing_by_route, name="get_sailing_from_and_to"),
    path('routes', route.get_all, name="get_all_routes"),
    path('terminals', terminal.get_all, name="get_all_terminals"),
]
