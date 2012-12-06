
"""
    plot-interesting.py <airport-code> [<start> [<finish>]]
        similar to plot-deviation.py, but makes use of REST tweets pulled in as a result of
        interesting people collection to hopefully recognize more individuals as ill.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import couchdb
import csv
from datetime import datetime, timedelta
import re

def key_to_datetime(key):
    return datetime(*key[1:])

def offset_to_key(origin, day_diff):
    d = origin + timedelta(days = day_diff)
    return [airport, d.year, d.month, d.day]

def min_union(a, b):
    return min(set(a) | set(b))

def max_union(a, b):
    return max(set(a) | set(b))

def dev_percent(val, avg):
    return (val - avg) * 100 / avg

""" init cmdline args and whatnot """
airport = sys.argv[1]
start, finish = None, None
start_str = sys.argv[2] if len(sys.argv) >= 3 else "2012-11-11"
finish_str = sys.argv[3] if len(sys.argv) >= 4 else datetime.utcnow().strftime("%Y-%m-%d")
start, finish = datetime.strptime(start_str, "%Y-%m-%d"), datetime.strptime(finish_str, "%Y-%m-%d")
# we need to keep track of this so the statistics for the first week of collection aren't skewed
collect_start = datetime(2012, 11, 17)
# catch input errors:
#   - quit if start date is not a sunday (week start)
#   - quit if finish comes before start
if start.weekday() != 6:
    print "ERROR: start date must be on a Sunday. (google flu trends limitation)"
    sys.exit(0)
if start >= finish:
    print "ERROR: start date must come before end date."
    sys.exit(0)
region_map = {}
gft_keys,   gft_values,   gft_sum,   gft_count   = {}, {}, 0, 0
couch_keys, couch_values, couch_sum, couch_count = {}, {}, 0, 0
health_threshold = 0.8

""" init couchdb stuff """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_airports = couch['airport_tweets']

""" read in airport -> region mapping """
with open('airport-to-city.txt', 'r') as rmap_file:
    line = rmap_file.readline()
    while line != "":
        code, region = line[0:3], re.sub(r'[\"]', r'', line[4:]).strip()
        region_map[code] = region
        gft_keys[code] = []
        gft_values[code] = []
        couch_keys[code] = [offset_to_key(start, i * 7) for i in range((finish - start).days / 7 + 1)]
        couch_values[code] = [0.0 for i in range((finish - start).days / 7 + 1)]
        line = rmap_file.readline()

""" retrieve stats from google flu trends csv """
with open('flu-trends.txt') as gft_file:
    for row in csv.DictReader(gft_file):
        week = datetime.strptime(row['Date'], "%Y-%m-%d")
        if week >= start and week <= finish:
            value = 0
            try:
                region = region_map[airport]
                key = [airport, week.year, week.month, week.day]
                value = int(row[region]) # this will throw valerror on ""
                gft_keys[airport].append(key)
                # note: takes average over week
                gft_values[airport].append(value / 7)
                gft_sum += value / 7
                gft_count += 1
            # ignore omitted data values
            except ValueError:
                pass

""" retrieve stats from couch db """
start_key = [airport, start.year, start.month, start.day]
end_key = [airport, finish.year, finish.month, finish.day]
query_later = []
query_for = {}
query_days = {}
print "startkey: %s" % start_key
print "endkey: %s" % end_key
results = db_airports.view(
    "Tweet/by_airport",
    startkey = start_key,
    endkey = end_key,
    include_doc = True)
for row in results:
    key, value, doc = row.key, row.value, row.doc
    #print "%s: %s" % (row.key, row.value)
    result_day = key_to_datetime(key)
    # if this tweet indicates sickness, do standard thing
    if doc.health >= health_threshold:
        index = (result_day - start).days / 7
        # weight sum properly if this result was between collection start and the next sunday
        if result_day >= collect_start and result_day < collect_start + timedelta(days = 1):
            print "next_week: %s" % (collect_start + timedelta(days = 1))
            couch_values[airport][index] += 1.0 / 1
        else:
            couch_values[airport][index] += 1.0 / 7
        couch_sum += 1.0
    # else append the from_user_id_str to list to query later
    else:
        query_later.append(doc.from_user_id_str)
        if not(doc.from_user_id_str in query_for):
            query_for[doc.from_user_id_str] = []
        query_for[doc.from_user_id_str].append(result_day)
        query_days[doc.from_user_id_str] = []

""" query across all users who MIGHT be sick """
# do several large queries instead of many many smaller ones
# this will give us excess data but will be a helluva lot faster
query_later.sort()
step = 100
for i in range(0, len(query_later), step):
    start, finish = query_later[i], query_later[min(i + step, len(query_later))]
    print "Querying from user %s to user %s" % (start, finish)
    results = db_airports.view("Tweet/by_user_id", startkey = start, endkey = finish, include_doc = True)
    for row in results:
        key, value, doc = row.key, row.value, row.doc
        if key in query_later:
            # if health is above threshold, add previous two days and next two days
            if doc.health >= health_threshold:
                print "\tFound sick tweet from user %s at time %s" % (doc.from_user_id_str, doc.created_at)
                sick_day = datetime.strptime(doc.created_at, '%a %b %d %H:%M:%S +0000 %Y %Z')
                for risk_day in (sick_day + timedelta(days = n) for n in range(-2, 3)):
                    if not(risk_day in query_days[doc.from_user_id_str]):
                        query_days[doc.from_user_id_str].append(risk_day)
# now that querying is complete, check whether users were actually sick on those days
for user in query_later:
    for day in query_for[user]:
        if day in query_days[user]:
            index = (result_day - start).days / 7
            # weight sum properly if this result was between collection start and the next sunday
            if day >= collect_start and day < collect_start + timedelta(days = 1):
                couch_values[airport][index] += 1.0 / 1
            else:
                couch_values[airport][index] += 1.0 / 7
            couch_sum += 1.0

# also account for collection start here
couch_count = (finish - max(start, collect_start)).days + 1

""" create lists for percent deviations """
gft_avg, couch_avg = float(gft_sum) / gft_count, float(couch_sum) / couch_count
print "Flu trends... sum: %s, count: %s, average: %s" % (gft_sum, gft_count, gft_avg)
print "Couch... sum: %s, count: %s, average: %s" % (couch_sum, couch_count, couch_avg)
print "Couch vals: %s" % couch_values[airport]
gft_pct = [dev_percent(v, gft_avg) for v in gft_values[airport]]
couch_pct = [dev_percent(v, couch_avg) for v in couch_values[airport]]

""" create histogram buckets for each dataset, then pdf """
figure = plt.figure()
axes = figure.add_subplot(111)
gft_times = [key_to_datetime(key) for key in gft_keys[airport]]
couch_times = [key_to_datetime(key) for key in couch_keys[airport]]
gft_line = axes.plot_date(gft_times, gft_pct, 'r-', linewidth = 1)
couch_line = axes.plot_date(couch_times, couch_pct, 'b-', linewidth = 1)

""" plot styling """
axes.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday = 6))
axes.xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
axes.xaxis.set_minor_locator(mdates.DayLocator())
axes.set_xlabel('Day')
axes.set_ylabel('% Deviation from Average')
axes.set_xlim(start, finish)
axes.set_ylim(min(-100.0, min_union(gft_pct, couch_pct)), max(100.0, max_union(gft_pct, couch_pct)))
axes.grid(True)

plt.savefig("figures/%s_idev.png" % airport,  dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
