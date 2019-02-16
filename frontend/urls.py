from django.urls import path, re_path
from . import views

# We only have a single view for the front end, as React handles the pages
urlpatterns = [
    re_path(r'(.*)$', views.app )
]
