
"""
    plot-test.py [airport-code] [start]
        confirms it works.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import couchdb
import csv
from datetime import datetime, timedelta
import time
import re
import random

""" init cmdline args and whatnot """
airport = sys.argv[1]
start = datetime.strptime(sys.argv[2], "%Y-%m-%d")
region_map = {}
gft_bins = {}
couch_bins = {}

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
        gft_bins[code] = []
        couch_bins[code] = []
        line = rmap_file.readline()

""" retrieve stats from google flu trends csv """
gft_keys = []
with open('flu-trends.txt') as gft_file:
    for row in csv.DictReader(gft_file):
        week = datetime.strptime(row['Date'], "%Y-%m-%d")
        if week >= start:
            gft_keys.append([airport, week.year, week.month, week.day])
            value = 0
            try:
                region = region_map[airport]
                value = int(row[region])
                # note: takes average over week
                gft_bins[airport].append(value / 7)
            except ValueError:
                pass

print "gft_keys: %s" % gft_keys
print "gft_bins: %s" % gft_bins

""" generate mock-up data """
def fts(offset):
    secs = offset * 24 * 60 * 60
    return start + timedelta(seconds = secs)

def key_to_datetime(key):
    return datetime(*key[1:])

ids = [[airport, fts(i).year, fts(i).month, fts(i).day] for i in range(14)]
vals = [np.random.randint(0, high = 50) for i in range(14)]
couch_keys = []
for i in range(14):
    row = { 'key': ids[i], 'value': vals[i] }
    print "%s: %s" % (row['key'], row['value'])
    couch_keys.append(row['key'])
    couch_bins[airport].append(row['value'])

print "couch_bins: %s" % couch_bins

""" create histogram buckets for each dataset, then pdf """
figure = plt.figure()
axes = figure.add_subplot(111)
gft_times = [key_to_datetime(key) for key in gft_keys]
couch_times = [key_to_datetime(key) for key in couch_keys]
print "gft_times: %s" % gft_times
print "couch_times: %s" % couch_times
gft_line = axes.plot_date(gft_times, gft_bins[airport], 'r-', linewidth = 1)
couch_line = axes.plot_date(couch_times, couch_bins[airport], 'b-', linewidth = 1)

""" plot styling """
axes.xaxis.set_major_locator(mdates.MonthLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
axes.xaxis.set_minor_locator(mdates.DayLocator())
axes.xaxis.set_major_formatter(mdates.DateFormatter('%a %d'))
axes.set_xlabel('Day')
axes.set_ylabel('# of Sick Individuals')
axes.set_xlim(start, datetime.now())
axes.grid(True)

figure.autofmt_xdate()
plt.savefig("figures/%s.svg" % airport,  dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
plt.show()
