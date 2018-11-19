from django.urls import path
from . import views
urlpatterns = [
    path('sailings', views.sailings ),
    path('ferries', views.ferries ),
]
