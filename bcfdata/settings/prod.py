from bcfdata.settings.base import *
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "postgres",
        'USER': "postgres",
        'PASSWORD': os.environ["DOKKU_POSTGRES_FERRYSTATUS_DB_ENV_POSTGRES_PASSWORD"],
        'HOST': os.environ["DOKKU_POSTGRES_FERRYSTATUS_DB_PORT_5432_TCP_ADDR"],
        'PORT': ''
    }
}

BASE_URL = "https://ferries.dokku.qc.nsnw.ca/"
SITE_ENV = "prod"
