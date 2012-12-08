"""
    meetings.py <file-path> [<distance-slack> <time-slack>]
"""

import couchdb
import cPickle as pickle
from datetime import datetime, timedelta
import logging
import sys

def couch_key_to_slice_key(couch_key):
    return "%s %04d-%02d-%02d" % (couch_key[0], couch_key[1], couch_key[2], couch_key[3])

def key_created_at(created_at):
    return datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S +0000')

def datetime_to_stamp(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def time_difference(a, b):
    a_time, b_time = key_created_at(a), key_created_at(b)
    sec_diff = abs((a_time - b_time).total_seconds())
    return float(sec_diff) / (60 ** 2)

""" distance in kilometers """
def calcDistanceOptimized(a, b):
    lat1, lon1 = a.coordinates
    lat2, lon2 = b.coordinates
    rad = 0.017453292519943
    yDistance = (lat2 - lat1) * 60.00721
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * 30.053965
    distance = math.sqrt( yDistance**2 + xDistance**2 )
    return distance * 1.85200088832

def new_meeting(a, b, meetings):
    return not ((a, b) in meetings) or ((b, a) in meetings)

""" start logging module """
logging.basicConfig(filename = 'meetings.log', level = logging.DEBUG, filemode = 'w')

""" grab cmdline args and initialize parameters """
file_name = sys.argv[1]
space_slack = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.1
time_slack = float(sys.argv[3]) if len(sys.argv) >= 4 else 1.0
collect_start = datetime(2012, 11, 17)
slice_table = {}
meetings = {}

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_airports = couch['airport_tweets']

""" grab all rows, place them in slicess """
results = db_airports.view("Tweet/meetings", include_docs = True)
logging.debug("Querying \"Tweet/meetings\" and slicing...")
for row in results:
    key, value, doc = row.key, row.value, row.doc
    stamp = couch_key_to_slice_key(key)
    if doc['created_at'] == None or doc['geo'] == None:
        continue
    if not stamp in slice_table:
        slice_table[stamp] = []
        meetings[stamp] = []
    slice_table[stamp].append((value, doc['created_at'], doc['geo']))
    logging.debug("\t[%s] <- (%s, %s, %s)" % (stamp, value, doc['created_at'], doc['geo']))

""" sort tweets across all slices, infer meetings """
logging.debug("\nSorting all slices and finding meetings...")
for (stamp, entries) in slice_table.items():
    # if we sort the list by time of tweet, we can reduce time significantly
    # ex: if timediff between (a = (..., noon, ...), b = (..., 3pm, ...)) is too great,
    # no need to check further than b for a meetings
    entries.sort(key = lambda entry: key_created_at(entry[1]))
    uno, dos, tres = [entry[1] for entry in entries[:3]]
    logging.debug("\tSorted entries by time. (sample: %s, %s, %s, ...)" % (uno, dos, tres))
    for i in range(len(entries)):
        for j in range(i, len(entries)):
            a, b = entries[i][0], entries[j][0]
            time_diff = time_difference(entries[i][1], entries[j][1])
            space_diff = calcDistanceOptimized(entries[i][2], entries[j][2])
            # output meeting and log if meeting hasn't already been added
            if time_diff <= time_slack and space_diff <= space_slack:
                if new_meeting(a, b, meetings[stamp]):
                    logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> YES!" % (a, b, time_diff, space_diff))
                    meetings[stamp].append((a, b))
                else:
                    logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> SKIP!" % (a, b, time_diff, space_diff))
            else:
                logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> NO!" % (a, b, time_diff, space_diff))
            # break if time slack exceeded
            if time_diff > time_slack:
                break

""" dump results to pickle """
logging.debug("\nDumping to file %s using cPickle." % file_name)
with open(file_name, 'w+') as pfile:
    pickle.dump(meetings, pfile)
logging.debug("\nDone! Exiting...")
