
"""
    plot-mobile.py <area-abbrev> [<start> [<finish>]]
        creates a plot of data that measures percent deviation from the average health score over
        time for Google Flu Trends and our mobile data.
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
    return [area, d.year, d.month, d.day]

def min_union(a, b):
    return min(set(a) | set(b))

def max_union(a, b):
    return max(set(a) | set(b))

def dev_percent(val, avg):
    return (val - avg) * 100 / avg

""" init cmdline args and whatnot """
area = sys.argv[1]
start, finish = None, None
start_str = sys.argv[2] if len(sys.argv) >= 3 else "2012-09-23"
finish_str = sys.argv[3] if len(sys.argv) >= 4 else datetime.utcnow().strftime("%Y-%m-%d")
start, finish = datetime.strptime(start_str, "%Y-%m-%d"), datetime.strptime(finish_str, "%Y-%m-%d")
# catch input errors:
#   - quit if start date is not a sunday (week start)
#   - quit if finish comes before start
if start.weekday() != 6:
    print "ERROR: start date must be on a Sunday. (google flu trends limitation)"
    sys.exit(0)
if start >= finish:
    print "ERROR: start date must come before end date."
    sys.exit(0)
region_map = {
    "BOS": "Boston, MA",
    "NYC": "New York, NY",
    "LA": "Los Angeles, CA",
    "SEA": "Seattle, WA",
    "SF": "San Francisco, CA"
}
gft_keys,   gft_values,   gft_sum,   gft_count   = {}, {}, 0, 0
couch_keys, couch_values, couch_sum, couch_count = {}, {}, 0, 0

""" init couchdb stuff """
couch = couchdb.Server('http://fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_mobile = couch['m']

""" read in airport -> region mapping """
for (code, region) in region_map.items():
    gft_keys[code] = []
    gft_values[code] = []
    couch_keys[code] = [offset_to_key(start, i * 7) for i in range((finish - start).days / 7 + 1)]
    couch_values[code] = [0.0 for i in range((finish - start).days / 7 + 1)]

""" retrieve stats from google flu trends csv """
with open('flu-trends.txt') as gft_file:
    for row in csv.DictReader(gft_file):
        week = datetime.strptime(row['Date'], "%Y-%m-%d")
        if week >= start and week <= finish:
            value = 0
            try:
                region = region_map[area]
                key = [area, week.year, week.month, week.day]
                value = int(row[region]) # this will throw valerror on ""
                gft_keys[area].append(key)
                # note: takes average over week
                gft_values[area].append(value / 7)
                gft_sum += value / 7
                gft_count += 1
            # ignore omitted data values
            except ValueError:
                pass

""" retrieve stats from couch db """
start_key = [area, start.year, start.month, start.day]
end_key = [area, finish.year, finish.month, finish.day]
print "startkey: %s" % start_key
print "endkey: %s" % end_key
results = db_mobile.view(
    "Tweet/by_closest_city_day",
    reduce = True,
    group = True,
    startkey = start_key,
    endkey = end_key)
for row in results:
    print "%s: %s" % (row.key, row.value)
    result_day = key_to_datetime(row.key)
    index = (result_day - start).days / 7
    # weight sum properly if this result was between collection start and the next sunday
    couch_values[area][index] += float(row.value) / 7
    couch_sum += row.value
# also account for collection start here
couch_count = (finish - start).days + 1
# trim leading zeros (some cities started collecting later than others)
while len(couch_values[area]) > 0 and couch_values[area][0] == 0.0:
    couch_values[area].pop(0)
    couch_keys[area].pop(0)
    couch_count -= 1

""" create lists for percent deviations """
gft_avg, couch_avg = float(gft_sum) / gft_count, float(couch_sum) / couch_count
print "Flu trends... sum: %s, count: %s, average: %s" % (gft_sum, gft_count, gft_avg)
print "Couch... sum: %s, count: %s, average: %s" % (couch_sum, couch_count, couch_avg)
print "Couch vals: %s" % couch_values[area]
gft_pct = [dev_percent(v, gft_avg) for v in gft_values[area]]
couch_pct = [dev_percent(v, couch_avg) for v in couch_values[area]]

""" create histogram buckets for each dataset, then pdf """
figure = plt.figure()
axes = figure.add_subplot(111)
gft_times = [key_to_datetime(key) for key in gft_keys[area]]
couch_times = [key_to_datetime(key) for key in couch_keys[area]]
gft_line = axes.plot_date(gft_times, gft_pct, 'r-', linewidth = 1)
couch_line = axes.plot_date(couch_times, couch_pct, 'b-', linewidth = 1)

""" plot styling """
axes.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday = 6))
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.xaxis.set_minor_locator(mdates.DayLocator())
axes.set_xlabel('Day')
axes.set_ylabel('% Deviation from Average')
axes.set_xlim(start, finish)
axes.set_ylim(min(-100.0, min_union(gft_pct, couch_pct)), max(100.0, max_union(gft_pct, couch_pct)))
axes.grid(True)

plt.savefig("figures/%s_mob.png" % area,  dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
