from . import response
from data.models import Ferry

def get_all(request):
    ferries = [
        ferry.as_dict for ferry in Ferry.objects.all().order_by('-last_updated')
    ]

    return response(request, ferries)
