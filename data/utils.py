import requests
import re
import logging
import pytz
from time import sleep
from bs4 import BeautifulSoup
from django.conf import settings
from collections import deque
from dateutil.parser import parse
from datetime import datetime, timedelta
from .models import (Terminal, Route, Ferry, Sailing, Destination, Status,
                     SailingEvent, ArrivalTimeEvent, ArrivedEvent, StatusEvent,
                     FerryEvent, DepartureTimeEvent, DepartedEvent,
                     PercentFullEvent, CarWaitEvent, OversizeWaitEvent,
                     InPortEvent, UnderWayEvent, OfflineEvent, HeadingEvent,
                     DestinationEvent, StoppedEvent, CancelledEvent,
                     ParkingEvent, CarPercentFullEvent,
                     OversizePercentFullEvent)

from collector.models import (ConditionsRun, DeparturesRun, LocationsRun,
                              SailingDetailRun, ConditionsRawHTML, DeparturesRawHTML,
                              LocationsRawHTML)

logger = logging.getLogger(__name__)

timezone = pytz.timezone("America/Vancouver")


def get_local_time(timestamp):
    return timezone.localize(timestamp).strftime("%H:%M")


def get_local_day():
    return datetime.now().astimezone(timezone).strftime("%Y-%m-%d")


def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count/2))]
    else:
        return sum(values[count/2-1:count/2+1])/2.0


def get_actual_departures(input_file: str=None) -> bool:
    """ Pull data from actualDepartures.asp page on the BC Ferries website.

    This will query https://orca.bcferries.com/cc/marqui/actualDepartures.asp
    and parse it. This page is an overview of all the routes BC Ferries
    provides information for.

    :param input_file: optional local file to read from
    :type input_file: str
    :returns: whether it succeeded or failed
    :rtype: bool
    """

    # Start a DeparturesRun
    run = DeparturesRun()
    # Build the URL to pull data from
    url = "{}/{}".format(settings.BCF_BASE_URL, "actualDepartures.asp")

    if input_file:
        # If an input file is given, read from that instead
        fp = open(input_file, 'r')
        data = fp.read()
    else:
        try:
            # Request page
            logger.info("Querying BCF for data...")
            response = requests.get(url)
            if response.status_code == 200:
                logger.debug("Successfully queried BCF for data")
                data = response.text
            else:
                # Something went wrong - log that it went wrong and return
                # TODO - fixup status
                logger.error("Could not retrieve details from the BC Ferries website: {}".format(response.status_code))
                run.status = "Could not retrieve details from the BC Ferries website (non-200 status code)"
                run.successful = False
                run.save()
                return False
        except:
            # TODO - replace bare except
            logger.error("Could not retrieve details from the BC Ferries website.")
            run.status = "Could not retrieve details from the BC Ferries website (unknown reason)"
            run.successful = False
            run.save()
            return False

    # Data retrieved
    run.set_status("Data retrieved from BCF")
    raw_html = DeparturesRawHTML(
        run=run,
        data=data
    )
    raw_html.save()

    # Load data into the BeautifulSoup parser
    b = BeautifulSoup(data, 'html.parser')

    # Parse out the routes
    # Create a deque object containing the routes and sailings
    routes = deque(
        b.find('td', class_='content').find('table').find_all('table')
    )

    # Parse out the current date
    date = b.find('span', class_='titleSmInv').text

    routes_list = []
    terminals = {}

    # Iterate over the routes
    while len(routes) != 0:
        # Pop off the next route
        route = routes.popleft()

        # Parse out the route name and the sailing time
        route_name, sailing_time = route.span.decode_contents().split('<br/>')

        # Parse out the source, destination, the source code and route code
        source, destination = re.search(r'(.*) to (.*)', route_name).groups()
        source_code, route_code = re.search(r'#([A-Z]+)(\d+)', route.find_previous_sibling().attrs['name']).groups()

        # Parse out the sailing time
        sailing_time = re.search("Sailing time: (.*)", sailing_time).groups()[0]

        # Some sailings (i.e. those to the Gulf Islands) are variable as BC Ferries doesn't provide live details for
        # them. For these, we can't get a duration - so skip them.
        if sailing_time != "Variable":
            # Sailing time is fixed, so parse out the hours and minutes for the duration
            times = re.search(r'(([0-9]+) hours?\s?)?(([0-9]+) minutes)?.*', sailing_time).groups()

            # Convert minutes to an integer
            if times[3]:
                minutes = int(times[3])
            else:
                minutes = 0

            # Convert hours to minutes
            if times[1]:
                minutes += int(times[1]) * 60

            logger.debug("Minutes: {}".format(minutes))

        # Add a mapping of terminal name to terminal source code
        terminals[source] = source_code

        # Pop off the sailings
        sailings = routes.popleft()

        # Create a dict with the details we've parsed out so far
        # TODO - minutes could potentially be unassigned
        route_details = {
            "source_code": source_code,
            "source": source,
            "destination": destination,
            "route_name": route_name,
            "route_code": route_code,
            "sailing_time": minutes
        }

        sailings_list = []

        # Iterate over the sailings
        for sailing in sailings.find_all('tr')[1:]:
            # Parse out the ferry, the scheduled departure time, the actual departure time, the ETA (or arrival time)
            # and the current status for this sailing
            ferry, scheduled, actual, eta_arrival, status = [td.text.strip() for td in sailing.find_all('td')]

            # Append the parsed details as a dict to our sailings list
            sailings_list.append({
                "ferry": ferry,
                "scheduled": scheduled,
                "actual": actual,
                "eta_or_arrival": eta_arrival,
                "status": status
            })

        route_details.update({"sailings": sailings_list})
        routes_list.append(route_details)

    # At this point, we've successfully parsed out the data from the HTML
    run.set_status("Data parsed")

    # Iterate over each route
    for route in routes_list:

        logger.debug("--- Parsing new route ---")

        # Get the source and destination name, and the source code
        destination_name = route['destination']
        source_name = route['source']
        source_code = route['source_code']

        # TODO - sailing_time is from above, probably shouldn't be here
        logger.debug("Sailing time is '{}'".format(sailing_time))

        # Get or create the Terminal object for the source
        source_o, created = Terminal.objects.get_or_create(
            name=source_name,
            short_name=source_code
        )

        # Log if we found or created a new Terminal object
        if created:
            logger.info("Created terminal {} for {}".format(
                source_code, source_name
            ))
        else:
            logger.debug("Found terminal {} for {}".format(
                source_o.name, source_o.short_name
            ))

        # See if the destination is a terminal, or just a description
        if destination_name not in terminals:
            logger.debug("{} not found in terminal list".format(destination_name))

            # Create Destination object without an associated terminal
            dest_o, created = Destination.objects.get_or_create(
                name=destination_name
            )

            # Log if we found or created a new Destination object
            if created:
                logger.info("Created destination for {}".format(
                    destination_name
                ))
            else:
                logger.debug("Found destination for {}".format(
                    dest_o.name
                ))
        else:
            # Get or create the Terminal object for the destination
            destination_o, created = Terminal.objects.get_or_create(
                name=destination_name,
                short_name=terminals[destination_name]
            )

            # Log if we found or created a new Terminal object for the destination
            if created:
                logger.info("Created terminal {} for {}".format(
                    destination_name, terminals[destination_name]
                ))
            else:
                logger.debug("Found terminal {} for {}".format(
                    destination_o.name, destination_o.short_name
                ))

            # Create Destination object (different to the actual Terminal
            # object for the destination)
            dest_o, created = Destination.objects.get_or_create(
                name=destination_name,
                terminal=destination_o
            )

            # Log if we found or created a new Destination object
            if created:
                logger.info("Created destination for {} ({})".format(
                    destination_name, destination_o
                ))
            else:
                logger.debug("Found destination for {} ({})".format(
                    dest_o.name, dest_o.terminal
                ))

        # Get the route code
        route_code = route['route_code']

        # Get or create a Route object for the route
        route_o, created = Route.objects.get_or_create(
            name=route['route_name'],
            source=source_o,
            destination=dest_o,
            route_code=route_code
        )

        # Log if we found or created a new Route object
        if created:
            logger.info("Created route {} ({} -> {})".format(
                route_o.route_code, route_o.source, route_o.destination
            ))
        else:
            logger.debug("Found route {} ({} -> {})".format(
                route_o.route_code, route_o.source, route_o.destination
            ))

        if not route_o.duration and route['sailing_time']:
            # We didn't previously have a duration for this route, but we do now - so update the Route object with it
            logger.debug("Setting sailing time to {}".format(route['sailing_time']))
            route_o.duration = route['sailing_time']
            route_o.save()

        # Iterate over the sailings for this route
        for sailing in route['sailings']:
            logger.debug(">>>>>> Parsing new sailing")
            ferry = sailing['ferry']
            scheduled_departure = sailing['scheduled']
            actual_departure = sailing['actual']
            eta_or_arrival = sailing['eta_or_arrival']
            status = sailing['status']

            # Get or create a Ferry object for this sailing's ferry
            ferry_o, created = Ferry.objects.get_or_create(
                name=ferry
            )

            # Log if we found or created a new Ferry object
            if created:
                logger.info("Created ferry {}".format(ferry))
            else:
                logger.debug("Found ferry {}".format(ferry))

            # Parse and convert the scheduled departure time
            # TODO - this shouldn't reuse the same name - it's ugly
            sched = parse("{} {}".format(date, scheduled_departure))
            sched = timezone.localize(sched)

            if actual_departure:
                # This sailing has left, so parse and convert the acual departure time...
                actual = parse("{} {}".format(date, actual_departure))
                actual = timezone.localize(actual)
                # ...and set the sailing to departed
                departed = True
            else:
                # No actual departure time found
                logger.debug("No actual departure time for this sailing")
                actual = None
                departed = False

            # Usefully (not), the ETA/arrival time can be '...' (unknown). We need to handle this gracefully
            if eta_or_arrival and eta_or_arrival is not '...':
                if 'ETA' in eta_or_arrival:
                    # We have an ETA, so parse it out
                    eta = re.search(r'ETA: (.*)', eta_or_arrival).groups()[0]
                    eta_or_arrival = parse("{} {}".format(date, eta))
                    eta_or_arrival = timezone.localize(eta_or_arrival)
                    logger.debug("ETA for this sailing is {}".format(eta_or_arrival))
                    # Since we have an ETA, this means this sailing hasn't arrived yet
                    arrived = False
                else:
                    # No ETA but an arrival time means this sailing has arrived
                    eta_or_arrival = parse("{} {}".format(date, eta_or_arrival))
                    eta_or_arrival = timezone.localize(eta_or_arrival)
                    logger.debug("Arrival time for this sailing was {}".format(eta_or_arrival))
                    arrived = True
            else:
                logger.debug("No ETA or arrival time")
                eta_or_arrival = None
                arrived = False

            # Get or create a Status object for this sailing
            status_o, created = Status.objects.get_or_create(
                status=status
            )

            # Log if we found or created a new Status object
            if created:
                logger.info("Created status {}".format(status))
            else:
                logger.debug("Found status {}".format(status))

            # Get or create a Sailing object for this sailing
            sailing_o, created = Sailing.objects.get_or_create(
                route=route_o,
                scheduled_departure=sched
            )

            # Log if we found or created a new Destination object
            if created:
                logger.info("Created sailing {}".format(sailing_o))
            else:
                logger.debug("Found sailing {}".format(sailing_o))

            # Since we track changes to the sailing, we now need to see if anything's changed between the details
            # we just parsed and the details we already had for this sailing

            # Check if the ferry has changed
            if sailing_o.ferry != ferry_o:
                # Ferry has changed
                logger.debug("Ferry has changed ({} to {})".format(
                    sailing_o.ferry, ferry_o
                ))

                # Create a FerryEvent
                event_o = FerryEvent(
                    sailing=sailing_o,
                    old_ferry=sailing_o.ferry,
                    new_ferry=ferry_o
                )
                sailing_o.ferry = ferry_o

                event_o.save()
                sailing_o.save()

            # Check if the actual departure time has changed (and yes, it can apparently)
            if sailing_o.actual_departure != actual:
                # Actual departure time has changed
                logger.debug("Actual departure has changed ({} to {})".format(
                    sailing_o.actual_departure, actual
                ))

                # Create a new DepartureTimeEvent
                event_o = DepartureTimeEvent(
                    sailing=sailing_o,
                    old_departure=sailing_o.actual_departure,
                    new_departure=actual
                )
                sailing_o.actual_departure = actual

                event_o.save()
                sailing_o.save()

            # Check if the sailing has departed (or un-departed - this can probably happen too)
            if sailing_o.departed != departed:
                # Departure status has changed
                logger.debug("Departed has changed ({} to {})".format(
                    sailing_o.departed, departed
                ))

                # Create a new DepartedEvent
                event_o = DepartedEvent(
                    sailing=sailing_o
                )
                sailing_o.departed = departed

                event_o.save()
                sailing_o.save()

            # Check if the ETA or arrival time has changed
            if sailing_o.eta_or_arrival_time != eta_or_arrival:
                # The ETA or arrival time has changed
                logger.debug("ETA or arrival time has changed ({} to {})".format(
                    sailing_o.eta_or_arrival_time, eta_or_arrival
                ))

                # Create a new ArrivalTimeEvent
                event_o = ArrivalTimeEvent(
                    sailing=sailing_o,
                    old_arrival=sailing_o.eta_or_arrival_time,
                    new_arrival=eta_or_arrival,
                    is_eta=not arrived
                )
                sailing_o.eta_or_arrival_time = eta_or_arrival

                event_o.save()
                sailing_o.save()

            # Check if the sailing has arrived
            if sailing_o.arrived != arrived:
                # Arrival status has changed
                logger.debug("Arrival has changed ({} to {})".format(
                    sailing_o.arrived, arrived
                ))

                # Create a new ArrivedEvent
                event_o = ArrivedEvent(
                    sailing=sailing_o
                )
                sailing_o.arrived = arrived

                event_o.save()
                sailing_o.save()

            # Check if the sailing status has changed
            if sailing_o.status != status_o:
                # Sailing status has changed
                logger.debug("Status has changed ({} to {})".format(
                    sailing_o.status, status_o
                ))

                # Create a new StatusEvent
                event_o = StatusEvent(
                    sailing=sailing_o,
                    old_status=sailing_o.status,
                    new_status=status_o
                )
                sailing_o.status = status_o

                # If the status is now Cancelled, additionally create a CancelledEvent
                # TODO - do we need to set the cancelled value here?
                if sailing_o.status == "Cancelled":
                    cancelled_o = CancelledEvent(
                        sailing=sailing_o
                    )
                    cancelled_o.save()

                event_o.save()
                sailing_o.save()

    # We've finished parsing and updating the departures information
    run.set_status("Completed", successful=True)
    logger.info("Finished retrieving and processing departures")
    return True


def get_current_conditions(input_file: str=None) -> bool:
    """ Pull data from the current conditions/"at-a-glance" page on the BC Ferries website.

    This will query https://orca.bcferries.com/cc/marqui/at-a-glance.asp and parse it. This
    page shows similar details to the actualDepartures.asp website, but shows some extra
    information, including how full the next few sailings are and how many car and oversize
    waits there are.

    :param input_file: optional local file to read from
    :type input_file: str
    :returns: whether it succeeded or failed
    :rtype: bool
    """

    # Start a ConditionsRun
    run = ConditionsRun()
    # Build the URL to pull data from
    url = "{}/{}".format(settings.BCF_BASE_URL, "at-a-glance.asp")

    if input_file:
        # If an input file is given, read from that instead
        # TODO - should be in a context
        fp = open(input_file, 'r')
        data = fp.read()
    else:
        try:
            # Request page
            logger.info("Querying BCF for data...")
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Successfully queried BCF for data")
                data = response.text
            else:
                # Something went wrong (i.e. we got something other than a 200 OK)
                logger.error("Could not retrieve details from the BC Ferries website: {}".format(response.status_code))
                run.set_status("Could not retrieve details from the BC Ferries website (non-200 status code)")
                run.successful = False
                run.save()
                return False
        except:
            # TODO - replace bare except
            logger.error("Could not retrieve details from the BC Ferries website.")
            run.set_status("Could not retrieve details from the BC Ferries website (unknown error)")
            run.successful = False
            run.save()
            return False

    # Data retrieved
    run.set_status("Data retrieved from BCF")
    raw_html = ConditionsRawHTML(
        run=run,
        data=data
    )
    raw_html.save()

    # Load data into the BeautifulSoup parser
    s = BeautifulSoup(data, 'html.parser')

    # TODO - this might be unused
    terminals = {}

    j_routes = []
    full_routes = []

    # Iterate over each section
    for section in s.find_all('tbody'):
        current_terminal = None
        if section.span:
            terminal_name = section.span.contents[0]
            terminal_id = terminal_name.lower().replace(' ', '_')
        else:
            # Parse out each sailing
            previously_parsed = None

            # Iterate over each sailing row
            for route in section.find_all('tr', recursive=False)[1:-1]:
                j_route = {}
                route_name = route.td.text
                details = route.find_all('td', recursive=False)

                fully_booked = False
                route_id = None

                try:
                    # Match the route ID
                    route_id = re.match('.*route=(\d+)&dept=(\w+).*', details[7].a.get('href')).groups()[0]
                except IndexError as e:
                    # If matching the above didn't work, it's possible the sailing is fully booked
                    if 'Vehicle space on this route is fully booked' in details[0].text:
                        logger.debug("All sailings today on the previously-parsed route are fully booked")
                        logger.debug("This was: {}".format(previously_parsed))
                        fully_booked = True
                        full_routes.append(previously_parsed)
                    else:
                        # Who knows?
                        logger.error("Unknown error: {}".format(e))

                if route_id:
                    # Store the route ID and route name
                    j_route['route_id'] = route_id
                    j_route['route_name'] = route_name

                    if details[1].div.text == "N/A":
                        # Sometimes the sailing details are "N/A" - so not much we can do with them
                        next_sailing = "N/A"
                        percent_full = "N/A"
                        j_route['sailings'] = None
                    else:
                        # Parse out each sailing
                        sailing_details = {}
                        sailings = details[1].div.table.find_all('tr')
                        j_sailings = []

                        # Iterate over each sailing
                        for sailing in sailings:
                            # Get the next sailing
                            next_sailing = sailing.td.text

                            # Check if the sailing has been cancelled
                            if sailing.td.next_sibling.text == "Cancelled":
                                # Sailing is cancelled
                                j_sailings.append({
                                    'time': next_sailing,
                                    'cancelled': True
                                })
                            else:
                                # Sailing isn't cancelled, so parse out how full this sailing is
                                percent_full = int(sailing.td.next_sibling.text.split('% ')[0])
                                sailing_details.update({next_sailing: percent_full})

                                j_sailings.append({
                                    'time': next_sailing,
                                    'percent_full': percent_full,
                                })

                        # Save this sailings
                        j_route['sailings'] = j_sailings

                        # Parse out the number of car and oversize waits
                        car_waits = int(details[2].text.rstrip('\n'))
                        oversize_waits = int(details[3].text.rstrip('\n'))

                        # ...and save those too
                        j_route['car_waits'] = car_waits
                        j_route['oversize_waits'] = oversize_waits

                    # Parse out later sailings. These are the ones which we don't have full
                    # details for yet
                    next_sailings = details[4].text.lstrip(' ').split(' ')
                    j_route['later_sailings'] = next_sailings

                    # Save all the sailings for this route
                    j_routes.append(j_route)
                    previously_parsed = route_name

    # Iterate over each route
    for route in j_routes:
        # Get the route name
        route_name = route['route_name']
        logger.debug("Found route {}".format(route_name))

        # Get the Route object for this route
        route_o = Route.objects.get(name=route_name)

        # Check if this route is full for today
        if route_name in full_routes:
            logger.debug("All of today's sailings are now full")

            # Set all of today's sailings to 100%
            for full_sailing in route_o.sailings_today:
                logger.debug("Setting sailing {} to 100% full...".format(
                    full_sailing
                ))

                # If this sailing wasn't previously full, set it to full
                if full_sailing.percent_full != 100:
                    logger.debug("Percent full has changed ({} -> {})".format(
                        full_sailing.percent_full, 100
                    ))

                    # Create a PercentFullEvent
                    percentfull_o = PercentFullEvent(
                        sailing=full_sailing,
                        old_value=full_sailing.percent_full,
                        new_value=100
                    )

                    full_sailing.percent_full = 100
                    full_sailing.save()

                    percentfull_o.save()
                else:
                    logger.debug("Sailing was already 100% full")

        # Get the car and oversize waits
        car_waits = route.get('car_waits', None)
        oversize_waits = route.get('oversize_waits', None)

        # Check if the waits have changed
        if route_o.car_waits != car_waits:
            # Car waits has changed
            logger.debug("Car waits has changed ({} -> {})".format(
                route_o.car_waits, car_waits
            ))

            # Create a CarWaitEvent
            carwaitevent_o = CarWaitEvent(
                route=route_o,
                old_value=route_o.car_waits,
                new_value=car_waits
            )

            route_o.car_waits = car_waits

            carwaitevent_o.save()
            route_o.save()

        if route_o.oversize_waits != oversize_waits:
            # Oversize waits has changed
            logger.debug("Oversize waits has changed ({} -> {})".format(
                route_o.oversize_waits, oversize_waits
            ))

            # Create a OversizeWaitEvent
            oversizewaitevent_o = OversizeWaitEvent(
                route=route_o,
                old_value=route_o.oversize_waits,
                new_value=oversize_waits
            )

            route_o.oversize_waits = oversize_waits

            oversizewaitevent_o.save()
            route_o.save()


        # Check if there are any sailings for this route today
        if not route['sailings']:
            # Nope :(
            logger.debug("No more sailings today for this route")
        else:
            # Iterate over each sailing
            for sailing in route['sailings']:
                logger.debug("Found sailing at {}".format(sailing['time']))

                # Build time
                today = datetime.now(timezone).strftime("%Y-%m-%d")
                sailing_time = parse("{} {}".format(
                    today,
                    sailing['time']
                ))
                sailing_time = timezone.localize(sailing_time)
                logger.debug("Sailing time is {}".format(sailing_time))

                # Find sailing
                sailing_o = Sailing.objects.get(
                    route=route_o,
                    scheduled_departure=sailing_time
                )

                # Check if the sailing was marked as cancelled
                if 'cancelled' in sailing:
                    logger.debug("Sailing has been cancelled")
                else:
                    # Get how full this sailing is
                    percent_full = sailing['percent_full']

                    # Check if the loading has changed
                    if sailing_o.percent_full != percent_full:
                        # Loading has changed
                        logger.debug("Percent full has changed ({} -> {})".format(
                            sailing_o.percent_full, percent_full
                        ))

                        # Create a PercentFullEvent
                        percentfull_o = PercentFullEvent(
                            sailing=sailing_o,
                            old_value=sailing_o.percent_full,
                            new_value=percent_full
                        )

                        sailing_o.percent_full = percent_full

                        percentfull_o.save()

                sailing_o.save()

        # For some sailings (i.e. Tsawwassen to Southern Gulf Islands) the
        # later sailings can actually include the day *after* tomorrow as
        # well as tomorrow - e.g. "*11:10am *5:40pm *9:05pm *9:55am". This
        # is as dumb as all hell but we have to handle it or we end up with
        # phantom sailings being created
        latest_time = None

        # Iterate over the later sailings
        for sailing in route['later_sailings']:
            logger.debug("Found later sailing {}".format(sailing))

            cancelled = False
            # Check if the sailing is cancelled
            if re.search('-Cancelled', sailing):
                # Sailing is cancelled
                logger.debug("Later sailing is cancelled")
                cancelled = True
                (sailing, _) = sailing.split('-')

            # Check if the sailing is tomorrow
            if sailing.startswith('*'):
                # Sailing is tomorrow
                tomorrow = (datetime.now(timezone) + timedelta(days=1)).strftime("%Y-%m-%d")
                sailing_time = parse("{} {}".format(
                    tomorrow, sailing[1:]
                ))
                sailing_time = timezone.localize(sailing_time)

                # Check for the aforementioned stupidity
                if latest_time and sailing_time < latest_time:
                    # Sailing is for the day after tomorrow
                    sailing_time = sailing_time + timedelta(days=1)
                    logger.debug("Later sailing is for the DAY AFTER tomorrow: {}".format(
                        sailing_time
                    ))
                    latest_time = sailing_time
                else:
                    # Sailing is for tomorrow
                    logger.debug("Later sailing is tomorrow: {}".format(
                        sailing_time
                    ))
                    latest_time = sailing_time

            else:
                # Sailing is today. Parse the time.
                today = datetime.now(timezone).strftime("%Y-%m-%d")
                sailing_time = parse("{} {}".format(
                    today, sailing
                ))
                sailing_time = timezone.localize(sailing_time)
                logger.debug("Later sailing is today: {}".format(
                    sailing_time
                ))
                latest_time = sailing_time

            # Get or create a Sailing object for this sailing
            sailing_o, created = Sailing.objects.get_or_create(
                route=route_o,
                scheduled_departure=sailing_time
            )

            # Check if a Sailing object was created
            if created:
                logger.info("Created sailing for {}".format(sailing_time))
            else:
                logger.debug("Sailing for {} already existed".format(sailing_time))

    # Parsing completed
    run.set_status("Completed", successful=True)
    logger.info("Finished retrieving and processing conditions")
    return True


def get_sailing_detail(input_file: str=None) -> bool:
    """ Pull data from the sailings detail page for each sailing.

    This will query the sailing detail page for each sailing, based on the routes that
    we know about.

    :param input_file: option local file to read from
    :type input_file: str
    :returns: whether we succeeded or failed
    :rtype: bool
    """

    # Set some useful variables for building the URLs
    URL_BASE = "https://orca.bcferries.com/cc/marqui"
    MAIN_PAGE = "{}/sailingDetail.asp".format(URL_BASE)

    # Start a SailingDetailRun
    run = SailingDetailRun()

    data = []
    if input_file:
        # If an input file was given, read from that
        with open(input_file, "r") as fp:
            file_data = fp.read()
            data.append(file_data)

    else:
        # For each route, query the sailing detail page
        for route in Route.objects.all():
            # Pad the route code with zeroes
            code = "{0:02d}".format(route.route_code)

            # Build the URL with the route code and source terminal
            url = "{}?route={}&dept={}".format(
                MAIN_PAGE, code, route.source.short_name
            )

            # Request pages
            try:
                logger.debug("Querying {}...".format(url))
                page = requests.get(url)
                data.append(page.content.decode())

                # Wait for 1 second so we don't hammer the BC Ferries website
                sleep(1)
            except Exception as e:
                # TODO - handle this better
                logger.error("Error ({}): {}".format(url, e))


    additional_urls = []
    # Iterate over the pages we've retrieved
    for d in data:
        # Load data into our BeautifulSoup parser
        b = BeautifulSoup(d, 'html.parser')

        # Check for the "No more scheduled sailings for today" message
        if "No more scheduled sailings for today" in d:
            logger.debug("No more URLs to retrieve")
        else:
            # Get additional sailing times
            for option in b.find('select').find_all('option'):
                additional_urls.append("{}/{}".format(
                    URL_BASE,
                    option['value']
                ))

    if not input_file:
        # If we're not reading from a local file, retrieve the additional sailings
        for additional_url in additional_urls:
            try:
                logger.debug("Querying {}...".format(additional_url))
                page = requests.get(additional_url)
                data.append(page.content.decode())

                # Again, sleep for 1 second so we don't hammer the website
                sleep(1)
            except Exception as e:
                # TODO - handle this exception better
                logger.error("Error ({}): {}".format(additional_url, e))

    # Iterate over the additional pages we've retrieved
    for d in data:
        # Load data into the parser
        b = BeautifulSoup(d, 'html.parser')

        # Parse out the route name and terminal code
        route_name = b.font.text
        terminal_code = re.search(r'.*arrivals-departures.html\?dept=(\w+)&.*', d).groups()[0]
        logger.debug("Terminal code: {}".format(terminal_code))
        logger.debug("Route name: {}".format(route_name))

        # Get the Route object, and the Terminal object for the source of this sailing
        route_o = Route.objects.get(name=route_name)
        terminal_o = Terminal.objects.get(short_name=terminal_code)

        # Check for the "No more scheduled sailings for today" message
        if 'No more scheduled sailings for today' in d:
            # No more sailings today
            logger.debug("No more scheduled sailings for today")
        else:

            # Parse the sailing details if they exist
            sailing_details = next(
                span.text for span in b.find_all('span') if 'Sailing Details' in span.text
            )

            # Parse the sailing time
            sailing_time = re.search(r'.*:\s(\S+ \w+)', sailing_details).groups()[0]
            logger.debug("Sailing time: {}".format(sailing_time))

            # Localise the scheduled departure time
            scheduled_departure = timezone.localize(parse("{} {}".format(
                get_local_day(),
                sailing_time
            )))
            logger.debug("Parsed timestamp: {}".format(scheduled_departure))

            # Get the Sailing object for this sailing. Since we should be running this after
            # the functions which pull the overall sailings information, this Sailing should
            # already exist.
            # TODO - should be a try/except
            sailing_o = Sailing.objects.get(
                route=route_o,
                scheduled_departure=scheduled_departure
            )

            # Check if the sailing is cancelled
            if "CANCELLED" in sailing_details:
                # Boo
                logger.debug("Sailing has been cancelled")
                sailing_o.cancelled = True

            else:
                # Get deck space
                car_space = None
                oversize_space = None
                try:
                    # Parse out the amount of deck space already committed by both cars
                    # and oversize vehicles
                    (oversize_space, car_space, timestamp) = re.search(
                        r'.*"DeckSpace_pop.asp\?os=(-?\d+)&uh=(-?\d+)&tm=(\d+)".*',
                        d).groups()
                    logger.debug("Car space used: {}".format(car_space))
                    logger.debug("Oversize space used: {}".format(oversize_space))

                    # Cast them to integers
                    car_percent = int(car_space)
                    oversize_percent = int(oversize_space)

                    # Check if the car deck space has changed
                    if sailing_o.car_percent_full != car_percent:
                        # Car deck space has changed
                        logger.debug("Car % was {}%, now {}%".format(
                            sailing_o.car_percent_full, car_percent
                        ))

                        # Create a new CarPercentFullEvent
                        car_event_o = CarPercentFullEvent(
                            sailing=sailing_o,
                            old_value=sailing_o.car_percent_full,
                            new_value=car_percent
                        )
                        car_event_o.save()

                        sailing_o.car_percent_full = car_percent

                    # Check if the oversize deck space has changed
                    if sailing_o.oversize_percent_full != oversize_percent:
                        # Oversize deck space has changed
                        logger.debug("Oversize % was {}%, now {}%".format(
                            sailing_o.oversize_percent_full, oversize_percent
                        ))

                        # Create a new OversizePercentFullEvent
                        oversize_event_o = OversizePercentFullEvent(
                            sailing=sailing_o,
                            old_value=sailing_o.oversize_percent_full,
                            new_value=oversize_percent
                        )
                        oversize_event_o.save()

                        sailing_o.oversize_percent_full = oversize_percent

                    sailing_o.save()

                except Exception as e:
                    # TODO - handle this better
                    # Couldn't find the deck space details
                    logger.warning("Couldn't find deck space usage: {}".format(
                        e
                    ))

                # Parse the ferry for this sailing, and load the corresponding Ferry object
                ferry = next(a.text for a in b.find_all('a') if 'onboard' in a['href'] and a.text)
                ferry_o = Ferry.objects.get(name=ferry)
                logger.debug("Ferry: {}".format(ferry))

        # Parse out the parking available at the source terminal
        parking = int(re.search(r'\s(\d+)%.*', next(td.text for td in b.find_all('td') if (len(td.find_all('a')) == 1 and td.a.text == "Parking"))).groups()[0])
        logger.debug("Parking: {}".format(parking))

        # Check if the amount of parking available has changed
        if terminal_o.parking != parking:
            # Available parking has changed
            logger.debug("Parking has changed from {}% to {}%".format(
                terminal_o.parking, parking
            ))

            # Create a new ParkingEvent
            parking_o = ParkingEvent(
                terminal=terminal_o,
                old_value=terminal_o.parking,
                new_value=parking
            )
            parking_o.save()
            terminal_o.parking = parking
            terminal_o.save()

    run.set_status("Completed", successful=True)
    logger.info("Finished retrieving and processing sailing details pages")
    return True


def get_ferry_locations() -> bool:
    """ Pull data on the ferry locations from the BC Ferries website.

    This will pull the popups that show the locations of the ferries.

    :returns: whether we succeeded or not
    :rtype: bool
    """

    # Set base URL and route numbers
    MAP_BASE = "https://orca.bcferries.com/cc/settings/includes/maps/"
    route_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '13']

    # Start a new LocationsRun
    run = LocationsRun()

    routes = {}
    # Iterate over the route numbers
    for i in route_numbers:
        # Build URL for this route
        url = "{}/route{}.html".format(MAP_BASE, i)
        run.set_status("Querying for locations: {}".format(url))

        try:
            # Query for data
            logger.info("Querying BCF for data...")
            response = requests.get(url)
            if response.status_code == 200:
                # Success!
                logger.info("Successfully queried BCF for data")
                # Store the page
                routes[i] = response.text
                raw_html = LocationsRawHTML(
                    run=run,
                    data=response.text,
                    url=url
                )
                raw_html.save()
            else:
                # Got a non-200 OK response
                logger.error("Could not retrieve details from the BC Ferries website: {}".format(response.status_code))
                run.set_status("Could not retrieve details from the BC Ferries website (non-200 status code)")
                return False
        except Exception as e:
            # TODO - handle this better
            logger.error("Could not retrieve details from the BC Ferries website. {}".format(e))
            run.set_status("Could not retrieve details from the BC Ferries website (non-200 status code)")
            return False

    run.set_status("Data retrieved from BCF")
    #routes.append(open("_data/route0.html", "r").read())

    # Iterate over each route
    for route_number in routes:
        # Retrieve page
        data = routes[route_number]

        # Parse page
        b = BeautifulSoup(data, 'html.parser')

        # Iterate over the page table
        for tr in b.body.table.find_all('tr')[1:]:
            # We only want rows with 4 entries - these are the ones with the ferry details
            if len(tr.find_all('td')) == 4:
                # Parse out the ferry name, status, destination and the last updated time
                (ferry, status, destination, time) = [e.text for e in tr.find_all('td')]
                logger.debug("Found {} (-> {}, {} @ {})".format(
                    ferry, destination, status, time
                ))

                # Localise the times
                now = datetime.now(timezone)
                today = now.strftime("%Y-%m-%d")
                updated_time = parse("{} {}".format(today, time))
                updated_time = timezone.localize(updated_time)

                # Handle times that were yesterday
                if updated_time > now:
                    logger.debug("Updated time was yesterday")
                    yesterday = (datetime.now(timezone) - timedelta(days=1)).strftime("%Y-%m-%d")
                    updated_time = parse("{} {}".format(yesterday, time))
                    updated_time = timezone.localize(updated_time)

                # Get or create a Ferry object for this ferry
                ferry_o, created = Ferry.objects.get_or_create(
                    name=ferry
                )

                # Check if a Ferry object was created
                if created:
                    logger.info("Created Ferry {}".format(ferry))

                # Handle route 2 and route 13 - these show a heading instead of a destination
                if route_number in ['2', '13']:
                    heading = destination

                    # Check if the heading has changed
                    if ferry_o.heading != heading:
                        # Heading has changed
                        logger.debug("Heading changed from {} to {}".format(
                            ferry_o.heading, heading
                        ))

                        # Create a new HeadingEvent
                        event_o = HeadingEvent(
                            ferry=ferry_o,
                            old_value=ferry_o.heading,
                            new_value=heading
                        )
                        event_o.save()

                        ferry_o.heading = heading
                        ferry_o.last_updated = updated_time
                        ferry_o.save()

                else:
                    # Get Destination object for the sailing destination
                    dest_o = Destination.objects.get(name__startswith=destination)

                    # Check if the destination has changed
                    if ferry_o.destination != dest_o:
                        # Destination has changed
                        logger.debug("Destination changed from {} to {}".format(
                            ferry_o.destination, dest_o
                        ))

                        # Create a new DestinationEvent
                        event_o = DestinationEvent(
                            ferry=ferry_o,
                            destination=dest_o,
                            last_updated=time
                        )
                        event_o.save()

                        ferry_o.destination = dest_o
                        ferry_o.last_updated = updated_time
                        ferry_o.save()

                # Check if the status has changed
                if ferry_o.status != status:
                    # Status has changed
                    logger.debug("Status changed from {} to {}".format(
                        ferry_o.status, status
                    ))

                    # Create events based on the new status
                    if status == "In Port":
                        event_o = InPortEvent(
                            ferry=ferry_o,
                            last_updated=updated_time
                        )
                        event_o.save()
                    elif status == "Under Way":
                        event_o = UnderWayEvent(
                            ferry=ferry_o,
                            last_updated=updated_time
                        )
                        event_o.save()
                    elif status == "Stopped":
                        event_o = StoppedEvent(
                            ferry=ferry_o,
                            last_updated=updated_time
                        )
                        event_o.save()
                    elif status == "Temporarily Off Line":
                        event_o = OfflineEvent(
                            ferry=ferry_o,
                            last_updated=updated_time
                        )
                        event_o.save()
                    else:
                        logger.warning("Unknown status: {}".format(status))

                    ferry_o.status = status
                    ferry_o.last_updated = updated_time
                    ferry_o.save()

    run.set_status("Completed", successful=True)
    logger.info("Finished retrieving and processing locations")
    return True
