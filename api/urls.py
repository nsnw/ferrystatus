from django.urls import path
from .views import ping, ferry, sailing

urlpatterns = [
    path('ping', ping, name="ping"),
    path('ferries', ferry.get_all, name="get_all_ferries"),
    path('sailings', sailing.get_all, name="get_all_sailings"),
    path('sailing/<int:sailing>', sailing.get_sailing, name="get_sailing"),
]
