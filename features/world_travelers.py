"""
    Finds number of individuals who have tweeted from the most airports.

    world_travelers.py <db-name> <file-path> <number-cutoff>

    example:
        python world_travelers.py airport_tweets world_travelers.txt 250
"""

import couchdb
import cPickle as pickle
from datetime import datetime, timedelta
import logging
import pprint
import sys

""" start logging module """
logging.basicConfig(filename = 'world_travelers.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" parse cmd line args and whatnot """
db_name = sys.argv[1]
file_name = sys.argv[2]
cutoff = int(sys.argv[3])

kv_pairs = []
travelers = []

""" init couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" find and order individuals by number of airports visited in time frame """
results = db.view('Tweet/user_airports', group = True)
for row in results:
    key, value = row.key, row.value.split(", ")
    kv_pairs.append((key, len(value)))
kv_pairs = sorted(kv_pairs, key = lambda kv: kv[1], reverse = True)
for i in range(min(cutoff, len(kv_pairs))):
    user, number = kv_pairs[i]
    sample = db.view('Tweet/by_user_id', key = user, include_docs = True, limit = 1)
    for row in sample:
        key, value, doc = row.key, row.value, row.doc
        travelers.append({
            'id': user,
            'name': doc['from_user_name'],
            'handle': doc['from_user'],
            'text': doc['text'],
            'num_visited': number })

""" pretty print it to file """
with open(file_name, 'w') as pfile:
    pp = pprint.PrettyPrinter(indent = 4, stream = pfile)
    pp.pprint(travelers)
