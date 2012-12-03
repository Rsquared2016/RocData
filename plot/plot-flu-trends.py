
"""
    plot-flu-trends.py [airport-code] [start]
        creates a best-fit line plot of data from the specified airport and Google Flu Trends data
        from the city that airport serves.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import couchdb
import csv
import datetime
import re

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
        code, region = line[0:3], re.sub(r'[\"]', r'', line[4:])
        region_map[code] = region
        gft_bins[code] = []
        couch_bins[code] = []
        line = rmap_file.readline()

""" retrieve stats from google flu trends csv """
with open('flu-trends.txt') as gft_file:
    for row in csv.DictReader(gft_file):
        week = datetime.strptime(row['Date'], "%Y-%m-%d")
        if week >= start:
            value = 0
            try:
                region = region_map[airport]
                value = int(row[region])
                # note: takes average over week
                gft_bins[airport].append(value / 7)
            except ValueError:
                pass

""" retrieve stats from couch db """
results = db_airports.view('Tweet/by_airport_day', reduce = True, group = True,
    startkey = (airport, start.year, start.month, start.day),
    endkey = (airport, (), (), ()))
for row in results:
    couch_bins[airport].append(row.value)

""" create histogram buckets for each dataset, then pdf """
figure = plt.figure()
axes = figure.add_subplot(111)
gft_hist, gft_edges = np.histogram(gft_bins[airport], len(gft_bins[airport]))
couch_hist, couch_edges = np.histogram(couch_bins[airport], len(couch_bins[airport]))
# use bin centers rather than bin edges
gft_center = 0.5 * (gft_edges[1:] + gft_edges[:-1])
couch_center = 0.5 * (couch_edges[1:] + couch_edges[:-1])
gft_bestfit = mlab.normpdf(gft_center)
couch_bestfit = mlab.normpdf(couch_center)
gft_line = axes.plot(gft_center, gft_bestfit, 'r', linewidth = 1)
couch_line = axes.plot(couch_center, couch_bestfit, 'b', linewidth = 1)

""" plot styling """
axes.set_xlabel('Time')
axes.set_ylabel('# of Sick Individuals')
axes.grid(True)

plt.show()
