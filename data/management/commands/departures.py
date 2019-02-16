from django.core.management.base import BaseCommand
from data.utils import get_actual_departures
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse departures"

    def add_arguments(self, parser):
        parser.add_argument('--input-file', help="optional input file")

    def handle(self, *args, **options):

        # Check if we've been passed a local file
        if 'input_file' in options:
            get_actual_departures(input_file=options['input_file'])
        else:
            get_actual_departures()
