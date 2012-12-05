
"""
    plot-deviation.py <airport-code> [<start> [<finish>]]
        creates a plot of data that measures percent deviation from the average health score over
        time for Google Flu Trends, our mobile data, and our airport data.
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
region_map = {}
gft_keys,   gft_values,   gft_sum,   gft_count   = {}, {}, 0, 0
couch_keys, couch_values, couch_sum, couch_count = {}, {}, 0, 0

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
        couch_keys[code] = [offset_to_key(start, i) for i in range((finish - start).days + 1)]
        couch_values[code] = [0 for i in range((finish - start).days + 1)]
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
print "startkey: %s" % start_key
print "endkey: %s" % end_key
results = db_airports.view(
    "Tweet/by_airport_day",
    reduce = True,
    group = True,
    startkey = start_key,
    endkey = end_key)
for row in results:
    print "%s: %s" % (row.key, row.value)
    index = (datetime(row.key[1], row.key[2], row.key[3]) - start).days
    print "(index): %s, (length): %s" % (index, len(couch_values[airport]))
    couch_keys[airport][index] = row.key
    couch_values[airport][index] = row.value
    couch_sum += row.value
couch_count = (finish - start).days

""" create lists for percent deviations """
gft_avg, couch_avg = float(gft_sum) / gft_count, float(couch_sum) / couch_count
print "Flu trends... sum: %s, count: %s, average: %s" % (gft_sum, gft_count, gft_avg)
print "Couch... sum: %s, count: %s, average: %s" % (couch_sum, couch_count, couch_avg)
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
axes.xaxis.set_major_locator(mdates.MonthLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
axes.xaxis.set_minor_locator(mdates.DayLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%a %d'))
axes.set_xlabel('Day')
axes.set_ylabel('% Deviation from Average')
axes.set_xlim(start, finish)
axes.set_ylim(min(-100.0, min_union(gft_pct, couch_pct)), max(100.0, max_union(gft_pct, couch_pct)))
axes.grid(True)

plt.savefig("figures/%s_dev.png" % airport,  dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
