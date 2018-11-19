from . import response
from data.models import Ferry

def get_all(request):
    ferries = [
        ferry.as_dict for ferry in Ferry.objects.all()
    ]

    return response(request, ferries)
