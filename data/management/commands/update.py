from django.core.management.base import BaseCommand
from data.utils import (get_actual_departures, get_current_conditions,
                        get_ferry_locations)
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse all information"

    def handle(self, *args, **options):
        get_actual_departures()
        get_current_conditions()
        get_ferry_locations()
