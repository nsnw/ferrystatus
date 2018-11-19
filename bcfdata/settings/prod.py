from bcfdata.settings.base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "postgres",
        'USER': "postgres",
        'PASSWORD': os.environ["DOKKU_POSTGRES_FERRIES_DB_ENV_POSTGRES_PASSWORD"],
        'HOST': os.environ["DOKKU_POSTGRES_FERRIES_DB_PORT_5432_TCP_ADDR"],
        'PORT': ''
    }
}

BASE_URL = "https://ferries.dokku.qc.nsnw.ca/"
SITE_ENV = "prod"
