from django.db.models import Q
from . import response, error
from data.models import Sailing
from datetime import datetime, timedelta

def get_all(request):
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    sailings = [
        sailing.as_dict for sailing in Sailing.objects.filter(
            Q(scheduled_departure__gt=now)|Q(eta_or_arrival_time__gt=hour_ago)
        ).order_by('scheduled_departure')
    ]

    return response(request, sailings)


def get_sailing(request, sailing: int):
    try:
        sailing = Sailing.objects.get(pk=sailing)
    except Sailing.DoesNotExist:
        return error(
            request,
            404,
            "Unknown sailing"
        )

    return response(request, sailing.as_dict)
