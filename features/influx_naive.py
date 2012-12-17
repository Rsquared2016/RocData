"""
    Calculates influx of sickness for all regions.
    Does not account for meetings yet, but will backtrack.

    influx_naive.py <db-name> <file-path> <health-threshold> <start-date> <end-date>

    example:
        python influx_naive.py airport_toy pickles/airport_toy_flux.pickle 0.8 2012-12-01 2012-12-09
"""

import couchdb
import cPickle as pickle
from datetime import datetime, timedelta
import logging
import pprint
import sys

def calculate_flux(date, airport):
    num_sick_today, num_sick_whole = 0.0, 0.0
    interval_length = (end_date - start_date).days + 1
    # sum over today and all days
    for day in flight_table.keys():
        for (source, stats) in flight_table[day][airport].items():
            if source == airport:
                continue
            num_sick_whole += float(stats['num_sick'])
            if day == date:
                num_sick_today += float(stats['num_sick'])
    try:
        return (num_sick_today / num_sick_whole) * interval_length
    except ZeroDivisionError as e:
        return 0.0

def update_flight_table(date, dest, src, sick, inc):
    if date not in flight_table:
        flight_table[date] = {}
    if dest not in flight_table[date]:
        flight_table[date][dest] = {}
    if src not in flight_table[date][dest]:
        flight_table[date][dest][src] = {
            'num_sick': 0,
            'num_flying': 0
        }
    if sick:
        flight_table[date][dest][src]['num_sick'] += inc
    flight_table[date][dest][src]['num_flying'] += inc

def update_flux_table(date, airport, flux):
    if date not in flux_table:
        flux_table[date] = {}
    if airport not in flux_table[date]:
        flux_table[date][airport] = 0.0
    flux_table[date][airport] = flux

def update_user_sick(user, date):
    if user not in user_sick:
        user_sick[user] = set()
    user_sick[user] |= set([date])

def user_sick_at_time(user, date):
    return ((user in user_sick) and (date in user_sick[user]))

def user_sick_over_time(user, start, finish):
    if start > finish:
        return False
    if user not in user_sick:
        return False
    for i in range((finish - start).days + 1):
        current = start + timedelta(days = i)
        if user_sick_at_time(user, current):
            return True
    return False

""" start logging module """
logging.basicConfig(filename = 'influx_naive.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" parse cmd line args and whatnot """
db_name = sys.argv[1]
file_name = sys.argv[2]
health_threshold = float(sys.argv[3])
dt = [int(d) for d in sys.argv[4].split('-')]
start_date = datetime(dt[0], dt[1], dt[2])
dt = [int(d) for d in sys.argv[5].split('-')]
end_date = datetime(dt[0], dt[1], dt[2])

regions = set()
times = set()
users = set()
flux_table = {}     # day: airport: total_flux
flight_table = {}   # day: dest: source: { num_flying, num_sick }
user_timelines = {} # user_id: [(region, time), ... ]
user_flights = {}   # user_id: [(src, dest, depart_time, arrival_time), ... ]
user_sick = {}      # user_id: set(date, ... )

""" init couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" get timeline information """
logging.debug("Querying \"Tweet/flights_to\" to find all regions...")
results = db.view("Tweet/flights_to", include_docs = True)
print "Tweets read from \"Tweet/flights_to\": %d" % len(results)
logging.debug("Got %s rows. (\"Tweet/flights_to\")" % len(results))
for row in results:
    user, time_str, region, doc = int(row.key[0]), row.key[1], row.value, row.doc
    date = datetime.strptime(time_str.split(" ")[0], "%Y-%m-%d")
    if date < start_date or date > end_date:
        continue
    # add any first encounters
    if date not in times:
        times |= set([date])
        flux_table[date] = {}
    if region not in regions:
        regions |= set([region])
        for day in flux_table.keys():
            flux_table[day][region] = 0.0
    if user not in users:
        users |= set([user])
        user_timelines[user] = []
    # add point to timeline
    user_timelines[user].append((region, date))
    # TODO: add some time range to this? 1 or 2 days in each direction?
    # also this will probably need to be moved once backtracking is added
    if doc['health'] >= health_threshold:
        logging.debug("\t[%s] User %s was sick on %s." % (region, user, time_str))
        update_user_sick(user, date)

if (end_date - start_date).days + 1 > len(times):
    print 'Not all requested days found in db.'
    exit(-1)

""" initialize flight and flux tables """
flux_table = { time: { airport: 0.0 for airport in regions } for time in times }
flight_table = { time: { dest: { src: { 'num_flying': 0, 'num_sick': 0 } for src in regions - set([dest]) } for dest in regions } for time in times }

""" build flight information """
logging.debug("\nConstructing flight information...")
for (user, timeline) in user_timelines.items():
    last_point = timeline[0]
    logging.debug("\tUser %s at %s on %s" % (user, last_point[0], last_point[1]))
    for point in timeline[1:]:
        region_now, time_now = point
        region_last, time_last = last_point
        logging.debug("\tUser %s at %s on %s" % (user, region_now, time_now))
        if region_now != region_last:
            logging.debug("\t\tUser %s flew %s -> %s (%s, %s)" % (user, region_last, region_now, time_last, time_now))
            if user not in user_flights:
                user_flights[user] = []
            user_flights[user].append((region_last, region_now, time_last, time_now))
        last_point = point

""" calculate total flying, sick flying """
logging.debug("\nCalculating aggregate flight statistics...")
for (user, flights) in user_flights.items():
    for flight in flights:
        source, destination, departure, arrival = flight
        # checks whether the user was sick over the entire flight time frame
        if user_sick_over_time(user, departure, arrival):
            logging.debug("\tUser %s was SICK on flight %s -> %s" % (user, source, destination))
            update_flight_table(arrival, destination, source, True, 1)
        else:
            logging.debug("\tUser %s was fine on flight %s -> %s" % (user, source, destination))
            update_flight_table(arrival, destination, source, False, 1)

""" calculate flux """
logging.debug("\nCalculating influx for all airports...")
for (date, airport_table) in flight_table.items():
    for airport in airport_table.keys():
        flux = calculate_flux(date, airport)
        update_flux_table(date, airport, flux)
        logging.debug("\tI(%s, %s): %f" % (date, airport, flux))

""" dump to pickle """
logging.debug("\nDumping to file %s using cPickle." % file_name)
with open(file_name, 'wb') as pfile:
    pickle.dump(flux_table, pfile, -1)
# for debugging!
with open(file_name + 'p', 'w') as pfile:
    pp = pprint.PrettyPrinter(indent = 4, stream = pfile)
    # remap flux_table: only emit entries with nonzero values
    flux_remap = {}
    for (date, table) in flux_table.items():
        flux_remap[date] = {}
        for (airport, flux) in table.items():
            if flux > 0.0:
                flux_remap[date][airport] = flux
    pp.pprint(flux_remap)
    #pp.pprint(flight_table)
logging.debug("\nDone! Exiting...")
