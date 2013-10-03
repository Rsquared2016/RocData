import couchdb
import datetime
import httplib
import json
import re
import signal
import sys
import time
import traceback
import urllib2
from twython import Twython
from extract_features import *
from socket import socket, SOCK_DGRAM, AF_INET

# Periodically download tweets from a given geographical area using Twitter search API
# Try multiple ways of figuring out the GPS coordinates of each tweet in this order:
#   1. Look for the "geo" tag
#   2. Extract GPS from the "location" tag
#   3. Feed the "location" tag into google maps geo-coder
# If all methods fail to find GPS, we set "lat" and "lon" to None
#
# Extract features from tweet text and feed them into SVM, which returns the "health" score
#
# Write the tweets, each augmented with "geo" and "health" tags, into couchdb

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
    status = { '_id': instance_id, 'num_tweets': numTweets, 'num_geo_tweets': numGeoTweets, 'num_non_geo_tweets': numNonGeoTweets, 'started_at': startTime, 'last_update': str(datetime.datetime.utcnow()), 'WORDS_file': WORDSfile, 'pause_time': pauseTime, 'geo_area': geo_area, 'db_name': dbName, 'geo_or_all': geoOrAll, 'SVM_file': SVMfile }
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
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    print "*** print_exc:"
    traceback.print_exc()
    print "*** format_exc, first and last line:"
    formatted_lines = traceback.format_exc().splitlines()
    print formatted_lines[0]
    print formatted_lines[-1]
    print "*** format_exception:"
    print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print "*** extract_tb:"
    print repr(traceback.extract_tb(exc_traceback))
    print "*** format_tb:"
    print repr(traceback.format_tb(exc_traceback))
    print "*** tb_lineno:", exc_traceback.tb_lineno

# Catch ctrl+C
def signal_handler(signal, frame):
    print "Tweets logged: %d" % numTweets
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def printTweet(tweet):
    if tweet['lat'] != None and tweet['lon'] != None:
        print('%03.4f %03.4f | %s... | %s' % (tweet['lat'], tweet['lon'], tweet['text'][0:80], tweet['from_user']))
    else:
        print('N/A      N/A     | %s... | %s' % (tweet['text'][0:80], tweet['from_user']))

def getInetIP():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(('google.com', 80))
    return s.getsockname()[0]

""" Read in WORDS """
WORDSfile = sys.argv[1]
pauseTime = float(sys.argv[2]) # seconds
geo_area = sys.argv[3]
dbName = sys.argv[4]
geoOrAll = sys.argv[5].strip().lower()
SVMfile = sys.argv[6]

ip_addr = getInetIP()
print ip_addr
instance_id = '%s (%s) @ %s' % (dbName, geoOrAll, ip_addr)

WORDStoID = readUniverseOfWords(WORDSfile)
model = loadSVM(SVMfile)

""" Instantiate couchdb """
couch = couchdb.Server('http://166.78.236.179:5984')
couch.resource.credentials = ('admin', 'admin')

# Write vital signals here
db_status = openOrCreateDb(couch, 'demon_status')

db = openOrCreateDb(couch, dbName)

""" Instantiate Twython with no Authentication """
twitter = Twython()

waitTime = 100 # seconds
lastID = 0
numTweets = 0
numGeoTweets = 0
numNonGeoTweets = 0
rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
pNewLine = re.compile('[\r\n]+')
p = re.compile('^#*[a-z]+\'*[a-z]*$')

startTime = str(datetime.datetime.utcnow())
updateVitals(db_status)
while True:
    try:
        search_results = twitter.searchTwitter(q="", rpp="100", lang="en", geocode=geo_area, since_id=str(lastID), result_type="recent")
    except: # catch all problems
        log('Error caught, continuing after %d seconds' % (waitTime))
        time.sleep(waitTime)
        twitter = Twython()
        continue
    try:
        e = search_results['error']
        log('Error caught: %s' % e)
        log('  Waiting for %d seconds' % waitTime)
        time.sleep(waitTime)
        twitter = Twython()
        continue
    except KeyError:
        pass

    if not(search_results.has_key("results")):
        log('Error caught: no "results" key')
        log('  Waiting for %d seconds' % waitTime)
        time.sleep(waitTime)
        twitter = Twython()
        continue

    for tweet in search_results["results"]:
        numTweets += 1
        if lastID < tweet["id"]:
            lastID = tweet["id"]

        # Extract GPS: try 'geo' tag, fallback to 'location' tag
        try:
            if len(tweet['geo']['coordinates']) != 2:
                tweet['geo'] = None
        except (KeyError, TypeError):
            tweet['geo'] = None
        if tweet['geo']==None and 'location' in tweet:
             match = rexLatLon.search(tweet['location'])
             if bool(match):
                 (lat, lon) = float(match.group('lat')), float(match.group('lon'))
                 tweet['geo'] = {'type': 'Point', 'coordinates': (lat, lon)}

        # Remove newlines
        tweet['text'] = re.sub(pNewLine, ' ', tweet['text']).encode("utf-8")

        # Classify tweet using SVM
        tweet['health'] = classifyTweetPython(tweet['text'], p, WORDStoID, model)

        # Save tweet GPS-tagged tweets and untagged tweets into separare dbs
        if tweet['geo'] != None:
            saveObjectToCouch(db, tweet)
            numGeoTweets += 1
        else:
            if geoOrAll == 'all':
                saveObjectToCouch(db, tweet)
                numNonGeoTweets += 1
        if numTweets % 500 == 0:
            #log('%d tweets logged (%d geo-tagged, %d non-geo-tagged)' % (numTweets, numGeoTweets, numNonGeoTweets))
            updateVitals(db_status)
    time.sleep(pauseTime)
