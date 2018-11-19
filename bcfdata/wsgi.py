import os
from django.core.wsgi import get_wsgi_application

env = os.environ.get("ENV", "prod")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcfdata.settings.{}".format(env))

application = get_wsgi_application()
