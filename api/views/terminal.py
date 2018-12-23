import logging
from pytz import timezone
from django.db.models import Q
from . import response, error
from data.models import Terminal
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_all(request):
    terminals = [
        terminal.as_dict for terminal in Terminal.objects.all()
    ]
    return response(request, terminals)
