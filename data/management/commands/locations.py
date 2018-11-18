from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, ProgrammingError
from data.models import Terminal, Route, Ferry, Sailing
from data.utils import get_ferry_locations
import logging
import os
import re
from datetime import datetime
from time import sleep

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse ferry locations"

    def handle(self, *args, **options):
        get_ferry_locations()
