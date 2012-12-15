"""
    Calculates influx of sickness for all regions.
    Does not backtrack or account for meetings yet.

    example:
        python influx_naive.py airport_toy pickles/airport_toy_flux.pickle 2012-12-01 2012-12-09
"""

import couchdb
import cPickle as pickle
from datetime import datetime, timedelta
import logging
import sys

""" start logging module """
logging.basicConfig(filename = 'influx_naive.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" parse cmd line args and whatnot """
db_name = sys.argv[1]
file_name = sys.argv[2]
dt = [int(d) for d in sys.argv[4].split('-')]
start_date = datetime(dt[0], dt[1], dt[2])
dt = [int(d) for d in sys.argv[5].split('-')]
end_date = datetime(dt[0], dt[1], dt[2])

regions = set()
times = set()
users = set()
flux_table = {}     # day: region: total_flux
user_timelines = {} # user_id: [(region, time), ... ]
user_flights = {}   # user_id: [(src, dest, depart_time, arrival_time), ... ]

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
    date = datetime.strptime(doc.key[1], "%Y-%m-%d %H:%M:%S")
    if date < start_date or date > end_date:
        continue
    # add any first encounters
    if date not in times:
        times |= set([date])
        flux_table[date] = {}
    if region not in regions:
        regions |= set([region])
    if user not in users:
        users |= set([user])
        user_timelines[user] = []
    # add point to timeline
    user_timelines[user].append((region, date))

if (end_date - start_date).days + 1 > len(times):
    print 'Not all requested days found in db.'
    exit(-1)

""" build flight information """
for (user, timeline) in user_timelines.items():
    last_point = timeline[0]
    for point in timeline[1:]:
        region_now, time_now = point
        region_last, time_last = last_point
        if region_now != region_last:
            if user not in user_flights:
                user_flights[user] = []
            user_flights[user].append((region_last, region_now, time_last, time_now))
        last_point = point

""" calculate total flying and stuff """

