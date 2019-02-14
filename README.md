# ferrystatus
User-friendly view of the status of BC Ferries sailings

This code will not run straight out of the box...

What this does:-

* scrapes the BC Ferries website for sailing statuses
* stores the results
* displays them in a nice, easy to read format

You can see this in action at https://ferrystatus.nsnw.ca/, although it may well be broken at any point.

# Getting a local version up and running

These instructions are brief and not at all complete. Here be dragons.

* Set up a virtualenv and install the Python dependencies with `pip install -r requirements.txt`
* Install NodeJS dependencies with `npm install`
* Build the frontend with `npm run all:dev`
* Run with `./manage.py runserver`

There's a few helpers that are set up as Django management commands. `./manage.py update` will go and pull the current data from the BC Ferries website and populate the database. In production, `worker.py` is run to periodically query the same data.
