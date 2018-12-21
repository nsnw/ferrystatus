from flask import Flask, request
from django.apps import apps
from django.conf import settings
from threading import Thread, Event
import os
from time import sleep
import logging
from datetime import datetime, timedelta
import pytz

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = "bcfdata.settings"

apps.populate(settings.INSTALLED_APPS)

from data.models import Sailing
from data.utils import (get_actual_departures, get_current_conditions,
                        get_ferry_locations, get_sailing_detail)

app = Flask(__name__)
last_run = datetime.utcfromtimestamp(0)
last_detail_run = datetime.utcfromtimestamp(0)

tz = pytz.timezone(settings.DISPLAY_TIME_ZONE)

interval = 600

def shutdown_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

def periodic_update():
    global last_run
    while e.is_set() is False:
        td = datetime.now() - last_run

        if td.seconds > 600:
            print("Querying departures...")
            get_actual_departures()
            print("Querying conditions...")
            get_current_conditions()
            print("Querying ferry locations...")
            get_ferry_locations()
            last_run = datetime.now()
        else:
            print("Sleeping ({} seconds to go)".format(interval - td.seconds))

        sleep(10)

    print("Shutdown worker")

def periodic_detail_update():
    global last_detail_run
    while e.is_set() is False:
        td = datetime.now() - last_detail_run

        if td.seconds > 3600:
            get_sailing_detail()
            last_detail_run = datetime.now()
        else:
            print("Sleeping ({} seconds to go)".format(3600 - td.seconds))

        sleep(10)

    print("Shutdown worker")


@app.route("/status")
def status():
    return str(last_run)


@app.route("/departures")
def departures():
    get_actual_departures()
    return "OK"


@app.route("/conditions")
def conditions():
    get_current_conditions()
    return "OK"


@app.route("/locations")
def locations():
    get_ferry_locations()
    return "OK"


@app.route("/update")
def update():
    get_actual_departures()
    get_current_conditions()
    get_ferry_locations()
    return "OK"


@app.route("/shutdown")
def shutdown():
    e.set()
    shutdown_flask()
    return "OK"


@app.route("/")
def index():
    return str(Sailing.objects.count())


e = Event()
t = Thread(target=periodic_update)
d = Thread(target=periodic_detail_update)
a = Thread(target=app.run, kwargs={
    "host": "0.0.0.0", "port": 6124
})

if __name__=='__main__':
    t.start()
    # d.start()
    a.start()
