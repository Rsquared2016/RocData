"""
    meetings.py <db-name> <file-path> <distance-slack-km> <time-slack-hours> <start-date> <end-date>

    example:
        python meetings.py airport_toy meetings_toy.pickle 0.1 1 2012-11-17 2012-12-9
"""

import couchdb
import cPickle as pickle
from datetime import datetime, timedelta
import logging
import pprint
import sys
import math

def key_created_at(created_at):
    return datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S +0000')

def time_difference(a, b):
    a_time, b_time = key_created_at(a), key_created_at(b)
    sec_diff = abs((a_time - b_time).total_seconds())
    return float(sec_diff) / (60 ** 2)

""" distance in kilometers """
def calcDistanceOptimized(a, b):
    lat1, lon1 = a['coordinates']
    lat2, lon2 = b['coordinates']
    rad = 0.017453292519943
    yDistance = (lat2 - lat1) * 60.00721
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * 30.053965
    distance = math.sqrt( yDistance**2 + xDistance**2 )
    return distance * 1.85200088832

def new_meeting(a, b, meetings):
    if not a in meetings or not b in meetings:
        return True
    return not (b in meetings[a] and a in meetings[b])

""" start logging module """
logging.basicConfig(filename = 'meetings.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" grab cmdline args and initialize parameters """
db_name = sys.argv[1]
file_name = sys.argv[2]
space_slack = float(sys.argv[3])
time_slack = float(sys.argv[4])
dt = [int(d) for d in sys.argv[5].split('-')]
start_date = datetime(dt[0], dt[1], dt[2])
dt = [int(d) for d in sys.argv[6].split('-')]
end_date = datetime(dt[0], dt[1], dt[2])

slice_table = {}
time_slices = set()
meetings = {}
users = set()

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" grab all rows, place them in slicess """
results = db.view("Tweet/meetings", include_docs = True)
print "Tweets read from view: %d" % len(results)
logging.debug("Got %s rows." % len(results))
logging.debug("Querying \"Tweet/meetings\" and slicing...")
for row in results:
    key, value, doc = row.key, row.value, row.doc
    date = datetime(key[1], key[2], key[3])
    time_slices.add(date)
    if doc['created_at'] == None or doc['geo'] == None or date < start_date or date > end_date:
        continue
    if not date in slice_table:
        slice_table[date] = []
        meetings[date] = {}
    if not value in users:
        users = users | set([value])
    slice_table[date].append((value, doc['created_at'], doc['geo']))
    logging.debug("\t[%s] <- (%s, %s, %s)" % (date, value, doc['created_at'], doc['geo']))


if (end_date-start_date).days+1 != len(time_slices):
    print 'Not all requested days found in db.'
    exit(-1)

print "Users: %s" % len(users)
""" sort tweets across all slices, infer meetings """
logging.debug("\nSorting all slices and finding meetings...")
for (date, entries) in slice_table.items():
    # if we sort the list by time of tweet, we can reduce time significantly
    # ex: if timediff between (a = (..., noon, ...), b = (..., 3pm, ...)) is too great,
    # no need to check further than b for a meetings
    entries.sort(key = lambda entry: key_created_at(entry[1]))
    samples = [entry[1] for entry in entries[:3]]
    logging.debug("\tSorted entries by time.")
    if len(samples) >= 3:
        logging.debug("sample: %s, %s, %s, ...)" % (samples[0], samples[1], samples[2]))
    for i in range(len(entries)):
        for j in range(i, len(entries)):
            a, b = int(entries[i][0]), int(entries[j][0])
            if a == b:
                continue
            time_diff = time_difference(entries[i][1], entries[j][1])
            space_diff = calcDistanceOptimized(entries[i][2], entries[j][2])
            # output meeting and log if meeting hasn't already been added
            if time_diff <= time_slack and space_diff <= space_slack:
                if new_meeting(a, b, meetings[date]):
                    logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> YES!" % (a, b, time_diff, space_diff))
                    if not a in meetings[date]:
                        meetings[date][a] = []
                    if not b in meetings[date]:
                        meetings[date][b] = []
                    meetings[date][a].append(b)
                    meetings[date][b].append(a)
                else:
                    logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> SKIP!" % (a, b, time_diff, space_diff))
            else:
                logging.debug("\t(%s, %s): [time: %.3f hr, space: %.3f km] -> NO!" % (a, b, time_diff, space_diff))
            # break if time slack exceeded
            if time_diff > time_slack:
                break

""" dump results to pickle """
logging.debug("\nDumping to file %s using cPickle." % file_name)
with open(file_name, 'wb') as pfile:
    pickle.dump(meetings, pfile, -1)
# for debugging!
#with open(file_name + 'p', 'w+') as pfile:
#    pp = pprint.PrettyPrinter(indent = 4, stream = pfile)
#    pp.pprint(meetings)
logging.debug("\nDone! Exiting...")
