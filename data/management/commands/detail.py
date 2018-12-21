from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, ProgrammingError
from data.models import Terminal, Route, Ferry, Sailing
from data.utils import get_sailing_detail
import logging
import os
import re
from datetime import datetime
from time import sleep

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse current conditions"

    def add_arguments(self, parser):
        parser.add_argument('--input-file', help="optional input file")

    def handle(self, *args, **options):

        if 'input_file' in options:
            get_sailing_detail(input_file=options['input_file'])
        else:
            get_sailing_detail()
