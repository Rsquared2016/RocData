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
from rtree import index
import sys
import math

def toUnix(dt):
    return int(dt.strftime('%s'))

def couch_key_to_slice_key(couch_key):
    return "%s %04d-%02d-%02d" % (couch_key[0], couch_key[1], couch_key[2], couch_key[3])

def key_created_at(created_at):
    return datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S +0000')

def time_difference(a, b):
    a_time, b_time = key_created_at(a), key_created_at(b)
    sec_diff = abs(toUnix(a_time) - toUnix(b_time))
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
    if (a not in meetings) or (b not in meetings):
        return True
    return not ((b in meetings[a]) and (a in meetings[b]))

def getTweetsNearGPSbyTimeWindow(date, point):
    try:
        dX, dY = degreesX, degreesY
        intersect = slice_indices[date].intersection((point[1] - dX, point[0] - dY, point[1] + dX, point[0] + dY), objects=True)
        return [n.object for n in intersect]
    except KeyError:
        return []

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
degreesY = (space_slack * 1000) * 0.00000900507679  # this many degrees make up 1 meter at NYC latitude
degreesX = (space_slack * 1000) * 0.00001183569359
numMeetings = 0

time_slices = set()
meetings = {}
users = set()
slice_indices = {}
slice_table = {}

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" grab all rows, place them in slicess """
results = db.view("Tweet/meetings", include_docs = True)
logging.debug("Querying \"Tweet/meetings\" and slicing...")
print "Tweets read from view: %d" % len(results)
logging.debug("Got %s rows." % len(results))
for row in results:
    key, value, doc = row.key, long(row.value), row.doc
    date = None
    if db_name == "nyc_one_month":
        date = datetime(key[0], key[1], key[2])
    else:
        date = datetime(key[1], key[2], key[3])
    #stamp = couch_key_to_slice_key(key)
    #time_slices.add(stamp)
    if doc['created_at'] == None or doc['geo'] == None or date < start_date or date > end_date:
        continue
    if not date in time_slices:
        #slice_table[stamp] = []
        time_slices.add(date)
        slice_indices[date] = index.Index()
        slice_table[date] = {}
        meetings[date] = {}
    if value not in users:
        users |= set([value])
    #slice_table[stamp].append((value, doc['created_at'], doc['geo']))
    lat, lng = doc['geo']['coordinates']
    slice_indices[date].insert(value, (lng, lat, lng, lat), obj = (value, doc['created_at'], doc['geo']))
    slice_table[date][value] = (value, doc['created_at'], doc['geo'])
    logging.debug("\t[%s] <- (%s, %s, %s)" % (date, value, doc['created_at'], doc['geo']))

if (end_date - start_date).days + 1 > len(time_slices):
    print 'Not all requested days found in db.'
    exit(-1)

print "Users: %s" % len(users)
logging.debug("\n%s users over %s time slices." % (len(users), len(time_slices)))
""" sort tweets across all slices, infer meetings """
logging.debug("\nFinding meetings across all time slices...")
for (date, slice_users) in slice_table.items():
    for (user, utup) in slice_users.items():
        uId, uCreated, uGeo = utup
        nearby_tweets = getTweetsNearGPSbyTimeWindow(date, uGeo['coordinates'])
        next_slice_tweets = getTweetsNearGPSbyTimeWindow(date + timedelta(days = 1), uGeo['coordinates'])
        nearby_tweets.extend(next_slice_tweets)
        logging.debug("\t%s @ %s: %d nearby tweets. %s" % (user, date, len(nearby_tweets), uGeo['coordinates']))
        for nearby_tweet in nearby_tweets:
            nId, nCreated, nGeo = nearby_tweet
            if uId == nId:
                continue
            time_diff = time_difference(uCreated, nCreated)
            if time_diff <= time_slack:
                if new_meeting(uId, nId, meetings[date]):
                    logging.debug("\t(%s, %s): [time: %.3f hr] -> YES!" % (uId, nId, time_diff))
                    if not uId in meetings[date]:
                        meetings[date][uId] = set()
                    if not nId in meetings[date]:
                        meetings[date][nId] = set()
                    meetings[date][uId] |= set([nId])
                    meetings[date][nId] |= set([uId])
                    numMeetings += 1
                else:
                    logging.debug("\t(%s, %s): [time: %.3f hr] -> SKIP!" % (uId, nId, time_diff))
            else:
                logging.debug("\t(%s, %s): [time: %.3f hr] -> NO!" % (uId, nId, time_diff))
print "%s meetings found." % numMeetings
logging.debug("%s meetings found." % numMeetings)

""" dump results to pickle """
logging.debug("\nDumping to file %s using cPickle." % file_name)
with open(file_name, 'wb') as pfile:
    pickle.dump(meetings, pfile, -1)
# for debugging!
#with open(file_name + 'p', 'w+') as pfile:
#    pp = pprint.PrettyPrinter(indent = 4, stream = pfile)
#    pp.pprint(meetings)
logging.debug("\nDone! Exiting...")
