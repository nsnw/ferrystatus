from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, ProgrammingError
from data.models import Terminal, Route, Ferry, Sailing
from data.utils import get_current_conditions
import logging
import os
import re
from datetime import datetime
from time import sleep

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Query and parse current conditions"

    def handle(self, *args, **options):
        get_current_conditions()
