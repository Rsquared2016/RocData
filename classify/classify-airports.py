
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

def updateVitals(db):
    status = {
        '_id': instance_id,
        'started_at': start_time,
        'last_update': str(datetime.datetime.utcnow()),
        'num_tweets': numTweets,
        'num_tweets_classified': numTweetsClassified,
        'WORDS_file': words_file,
        'db_name': dbname,
        'since': since,
        'SVM_file': svm_file }
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

# Catch ctrl+C
def signal_handler(signal, frame):
    print "Stopping execution, dumping table, updating vitals..."
    updateVitals(db_status)
    pfile = open(pickle_file, 'a+')
    pickle.dump(health_score_table, pfile)
    pfile.close()
    print "since: %s, num_tweets: %s, num_tweets_classified: %s" % (since, numTweets, numTweetsClassified)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

""" initialize cmdline args and other parameters """
pickle_file = sys.argv[1]
words_file = sys.argv[2]
svm_file = sys.argv[3]
last_time = int(datetime.datetime.utcnow().strftime("%s"))
dbname = 'classify_airports'
numTweets = 0
numTweetsClassified = 0
currentId = None
since = 1
health_score_table = {}
ip_addr = urllib2.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
instance_id = '%s (%s) @ %s' % (dbname, "N/A", ip_addr)
start_time = str(datetime.datetime.utcnow())
rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
pNewLine = re.compile('[\r\n]+')
p = re.compile('^#*[a-z]+\'*[a-z]*$')

""" load up SVM stuff """
WORDStoID = readUniverseOfWords(words_file)
model = loadSVM(svm_file)

""" load up pickle stuff """
pfile = open(pickle_file, 'a+')
try:
    for tweet, score in pickle.load(pfile).iteritems():
        health_score_table[tweet] = score
except EOFError:
    log("%s empty, continuing..." % pickle_file)
pfile.close()

""" couchdb stuff """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_status = openOrCreateDb(couch, 'demon_status')
db_airports = openOrCreateDb(couch, 'airport_tweets')
# try to grab the last update seq so we don't waste time reclassifying
status_doc = db_status.get(instance_id)
if status_doc != None:
    if 'since' in status_doc:
        since = status_doc['since']
    if 'num_tweets' in status_doc:
        numTweets = status_doc['num_tweets']
    if 'num_tweets_classified' in status_doc:
        numTweetsClassified = status_doc['num_tweets_classified']
updateVitals(db_status)
print "since: %s, num_tweets: %s, num_tweets_classified: %s" % (since, numTweets, numTweetsClassified)

if __name__ == "__main__":
    """ main program loop """
    while True:
        changes = db_airports.changes(feed = "longpoll", since = since, limit = 50)
        since = changes['last_seq']
        for change in changes['results']:
            if change['id'].find('_design') != -1:
                log("skipping over %s..." % tweet['_id'])
                continue
            tweet = None
            try:
                tweet = db_airports[change['id']]
            except couchdb.http.ResourceNotFound:
                log("could not load doc %s from database 'airport_tweets'." % change['id'])
                continue
            numTweets += 1
            if not (tweet['_id'] in health_score_table):
                health_score_table[tweet['_id']] = classifyTweetPython(tweet['text'], p, WORDStoID, model)
                log("classified tweet %s: %s" % (tweet['_id'], health_score_table[tweet['_id']]))
                numTweetsClassified += 1
            else:
                log("%s already classified: %s" % (tweet['_id'], health_score_table[tweet['_id']]))
            if numTweetsClassified % 50 == 0:
                updateVitals(db_status)
        pfile = open(pickle_file, 'a+')
        pickle.dump(health_score_table, pfile)
        pfile.close()
