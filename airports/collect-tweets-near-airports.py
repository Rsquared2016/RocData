
from twython import Twython
import urllib2
import time
import json
import signal
import sys
import httplib
import traceback
import couchdb
import datetime
import re

class Airport:
    def __init__(self, name, code, lat, lon):
        self.name = name
        self.code = code
        self.lat = lat
        self.lon = lon
    def __str__(self):
        return 'Airport %s (%s): [%f, %f]' % (code, name, lat, lon)

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def openOrCreateDb(server, name):
    try:
        db = server.create(name) # newly created
        return db
    except couchdb.http.PreconditionFailed:
        db = server[name]
        return db

def saveObjectToCouch(db, o):
    o['_id'] = o['id_str']
    try:
        db.save(o, batch='ok')
        return True
    except couchdb.http.ResourceConflict:
        print('Object with _id %s already in db; continuing...' % o['_id'])
        return False
    except (socket.error, couchdb.http.ServerError):
        print 'Caught error on db.save(), sleeping for a while...'
        time.sleep(60) # hope db comes back up
        return False

def updateVitals(db):
    status = {
        '_id': instance_id,
        'num_tweets': numTweets,
        'num_geo_tweets': numGeoTweets,
        'num_non_geo_tweets': numNonGeoTweets,
        'started_at': startTime,
        'last_update': str(datetime.datetime.utcnow()),
        'pause_time': pauseTime,
        'db_name': dbName,
        'geo_or_all': geoOrAll }
    try:
        doc = db[status['_id']]
        status['_rev'] = doc['_rev']
    except couchdb.http.ResourceNotFound:
        pass
    try:
        db.save(status, batch='ok')
    except (socket.error, couchdb.http.ServerError):
        time.sleep(60)
        pass

def printException():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print "*** print_exception:"
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
    print "*** print_exc:"
    traceback.print_exc()
    print "*** format_exc, first and last line:"
    formatted_lines = traceback.format_exc().splitlines()
    print formatted_lines[0]
    print formatted_lines[-1]
    print "*** format_exception:"
    print repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback))
    print "*** extract_tb:"
    print repr(traceback.extract_tb(exc_traceback))
    print "*** format_tb:"
    print repr(traceback.format_tb(exc_traceback))
    print "*** tb_lineno:", exc_traceback.tb_lineno

## --------------------------------------------------------------------------------
## Read airport data
input = open('airport-to-GPS-sorted-by-passenger-count.txt', 'r')
code2a = {}
codes = []
for line in input:
	columns = line.split('\t')
        code = columns[0]
        lat = float(columns[1])
        lon = float(columns[2])
        name = columns[3]
        code2a[code] = Airport(name, code, lat, lon)
        codes.append(code)
input.close()
#print codes

## --------------------------------------------------------------------------------
## Collect tweets

# Catch ctrl+C
def signal_handler(signal, frame):
        print 'Terminating, flushing file %s' % fileName
        log.close()
        print "Tweets logged: %d" % numTweets
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#Geo_area = "34.05,-118.25,150km" # Los Angeles
#geo_area = "43.165556,-77.611389,80km" # Rochester, NY
#geo_area = "40.716667,-74.00,100km" # NYC

dbName = 'airport_tweets'
lastID = []
numTweets = 0
numGeoTweets = 0
numNonGeoTweets = 0
gps = 0
location = 0
numSuccessfulQueries = 0
waitTime = 5 # minutes
rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
pNewLine = re.compile('[\r\n]+')

begin = int(sys.argv[1])
end = int(sys.argv[2])
pauseTime = float(sys.argv[3]) # minutes
geoOrAll = sys.argv[4].strip().lower()
print 'Collecting airports %d through %d' % (begin, end)

ip_addr = urllib2.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
instance_id = '%s (%s) @ %s' % (dbName, geoOrAll, ip_addr)

""" Instantiate Twython with no Authentication """
twitter = Twython()

""" instantiate couchdb connections """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_status = openOrCreateDb(couch, 'demon_status') 
db = openOrCreateDb(couch, dbName)

for a in range(begin,end+1):
    lastID.append(0)

startTime = str(datetime.datetime.utcnow())
updateVitals(db_status)

# NOTE: radius is tight enough that we are not worrying about intersections.
# if it expands, it's something to reconsider.
while True:
    for (i, a) in enumerate(range(begin,end+1)):
        airport = code2a[codes[a]]
        radius = '3km'
        geo_area = '%f,%f,%s' % (airport.lat, airport.lon, radius)

        # perform search over geographic area
        try:
            search_results = twitter.searchTwitter(q="", rpp="100", lang="en", geocode=geo_area, since_id=str(lastID[i]), result_type="recent")
        except: # catch all problems
            print 'Error caught, continuing after %d seconds' % (waitTime*60)
            print i, a
            printException()
            time.sleep(waitTime)
            twitter = Twython()
            continue

        #print search_results
        try:
            e = search_results['error']
            print 'Error caught: %s' % e
            print 'Waiting for %d minutes' % waitTime
            time.sleep(waitTime)
            continue
        except KeyError:
            numSuccessfulQueries += 1

        # stall if no results key came back
        if not(search_results.has_key("results")):
            log('Error caught: no "results" key')
            log('  Waiting for %d seconds' % waitTime)
            time.sleep(waitTime)
            twitter = Twython()
            continue

        for tweet in search_results["results"]:
            numTweets += 1
            if lastID[i] < tweet["id"]: 
                lastID[i] = tweet["id"]

            # Extract GPS: try 'geo' tag, fallback to 'location' tag
            if not('geo' in tweet) and tweet['location'] != None:
                 match = rexLatLon.search(tweet['location'])
                 if bool(match):
                     (lat, lon) = float(match.group('lat')), float(match.group('lon'))
                     tweet['geo'] = {'type': 'Point', 'coordinates': (lat, lon)}
            try:
                if len(tweet['geo']['coordinates']) != 2:
                    tweet['geo'] = None
            except (KeyError, TypeError):
                tweet['geo'] = None

            # Remove newlines
            tweet['text'] = re.sub(pNewLine, ' ', tweet['text']).encode("utf-8")
            # save airport code in the tweet
            tweet['airport'] = airport.code
            # save origin!
            tweet['origin'] = 'search'

            # persist tweets in database
            if geoOrAll == 'all' or tweet['geo'] != None:
                saveObjectToCouch(db, tweet)

            print '%s: %s' % (airport.code, tweet["text"])
            if numTweets % 500 == 0:
                updateVitals(db_status)
        sys.stdout.flush()
    time.sleep(pauseTime)





