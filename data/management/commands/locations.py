from django.core.management.base import BaseCommand
from data.utils import get_ferry_locations
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse ferry locations"

    def handle(self, *args, **options):
        get_ferry_locations()
