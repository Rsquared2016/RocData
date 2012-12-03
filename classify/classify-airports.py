
import couchdb
import datetime
import httplib
import json
import re
import signal
import socket
import sys
import time
import traceback
import urllib2
import pickle
from extract_features import *

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
    print o
    return
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

# Catch ctrl+C
def signal_handler(signal, frame):
    print "Stopping execution, dumping table, updating vitals..."
    updateVitals(db_status)
    print "since: %s, num_tweets: %s, num_tweets_classified: %s" % (currentIds, numTweets, numTweetsClassified)
    sys.stdout.flush()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

""" initialize cmdline args and other parameters """
words_file = sys.argv[1]
svm_file = sys.argv[2]
last_time = int(datetime.datetime.utcnow().strftime("%s"))
numTweets = 0
numTweetsClassified = 0
currentId = None
start_time = str(datetime.datetime.utcnow())
rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
pNewLine = re.compile('[\r\n]+')
p = re.compile('^#*[a-z]+\'*[a-z]*$')

""" load up SVM stuff """
WORDStoID = readUniverseOfWords(words_file)
model = loadSVM(svm_file)

""" couchdb stuff """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_airports = openOrCreateDb(couch, 'airport_tweets')
print "start_time: %s" % start_time
print "last_tweet: %s, num_tweets: %s, num_tweets_classified: %s" % (currentId, numTweets, numTweetsClassified)
if __name__ == "__main__":
    """ main program loop """
    #for row in db_airports.view('Tweet/no_health', include_docs = True):
    for row in db_airports.view('Tweet/no_health', include_docs = True):
        currentId = row.key
        tweet = row.doc
        numTweets += 1
        tweet['health'] = classifyTweetPython(tweet['text'], p, WORDStoID, model)
        numTweetsClassified += 1
        saveObjectToCouch(db_airports, tweet)
        if numTweetsClassified % 50 == 0:
            log("since: %s, num_tweets: %s, num_tweets_classified: %s" % (currentId, numTweets, numTweetsClassified))
    log("num_tweets: %s, num_tweets_classified: %s" % (numTweets, numTweetsClassified))
