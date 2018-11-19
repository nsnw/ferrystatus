from django.http import JsonResponse
from datetime import datetime


def response(request, data):
    now = datetime.now()

    response = {
        "meta": {
            "timestamp": now,
            "request": request.path
        },
        "response": data
    }
    return JsonResponse(response)


def error(request, status_code, error_text):
    now = datetime.now()

    response = {
        "meta": {
            "timestamp": now,
            "request": request.path
        },
        "error": error_text
    }
    return JsonResponse(response, status=status_code)


def ping(request):
    return JsonResponse({"status": "ok"})
