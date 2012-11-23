
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

"""
    Overview:
        - hit CouchDB for persons of interest: people who tweeted from more than airport
        - if we haven't seen this POI before, spin off a streaming API collector for them
        - mark all their tweets as interesting
        - MAYBE: construct timeline?
"""

""" DbManager: layer of frequently used operations over our couchdbs """
class DbManager:
    def __init__(self, name, server):
        self.db = None
        self.name = name
        self.server = server

    def open(self):
        try:
            self.db = self.server.create(self.name) # newly created
            return True
        except couchdb.http.PreconditionFailed:
            self.db = self.server[self.name]
            return False

    def save(self, doc):
        try:
            self.db.save(doc, batch='ok')
            return True
        except AttributeError:
            print('Database instance for "%s" has not been opened or created.' % self.name)
            return False
        except couchdb.http.ResourceConflict:
            print('Document %s in database conflicted during update.' % doc['_id'])
            print('Server revision: [%s], client revision: [%s]' % self.db[doc['_id']]['_rev'], doc['_rev'])
            return False
        except (socket.error, couchdb.http.ServerError):
            print 'Caught error on db.save(), ignoring.'
            return False

    def get(self, id):
        try:
            return self.db.get(id)
        except AttributeError:
            print('Database instance for "%s" has not been opened or created.' % self.name)
            return False

    def update_field(self, id, field, value):
        try:
            doc = self.db[id]
            doc[field] = value
            self.save(doc)
            return True
        except AttributeError:
            print('Database instance for "%s" has not been opened or created.' % self.name)
            return False

""" execute the script """
if __name__ == "__main__":
    """ initialize cmdline args and other parameters """
    pause_time = int(sys.argv[1])
    refresh_time = int(sys.argv[2])
    dbname = 'airport_tweets'
    numTweets = 0
    numGeoTweets = 0
    numNonGeoTweets = 0
    interestingPeople = []
    ip_addr = urllib2.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
    start_time = str(datetime.datetime.utcnow())
    username = 'corporaMine'
    password = 'tw1tterhea1th'
    rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
    pNewLine = re.compile('[\r\n]+')

    """ initialize Twython """
    twitter = Twython()

    """ initialize CouchDB stuff """
    couch = couchdb.Server('http://dev.fount.in:5984')
    couch.resource.credentials = ('admin', 'admin')
    db_status = DbManager('demon_status', couch)
    db_status.open()
    db_airport_tweets = DbManager(dbname, couch)
    db_airport_tweets.open()

    """ function for writing status """
    def updateVitals(db, name):
        idFor = '%s (%s) @ %s' % (name + '_interesting', "N/A", ip_addr)
        doc = db.get(idFor)
        try:
            status = {
                '_id': idFor,
                'num_tweets': numTweets,
                'num_geo_tweets': numGeoTweets,
                'num_non_geo_tweets': numNonGeoTweets,
                'started_at': start_time,
                'last_update': str(datetime.datetime.utcnow()),
                'pause_time': pause_time,
                'db_name': name }
            if doc != None:
                status['_rev'] = doc['_rev']
        except couchdb.http.ResourceNotFound:
            pass
        try:
            db.save(status)
        except (socket.error, couchdb.http.ServerError) as e:
            print "Couldn't write status to server: %s" % e
            sys.exit

    """ utility function for streaming -> search """
    def rest2search(stream):
        search = {}
        search['_id'] = stream['id_str']
        search['id'] = stream['id']
        search['id_str'] = stream['id_str']
        search['text'] = stream['text']
        search['source'] = stream['source']
        search['created_at'] = stream['created_at']
        search['geo'] = None
        if stream['geo'] != None:
            search['geo'] = stream['geo']
        search['metadata'] = None
        search['to_user'] = stream['in_reply_to_screen_name']
        search['to_user_id'] = stream['in_reply_to_user_id']
        search['to_user_id_str'] = stream['in_reply_to_user_id_str']
        search['to_user_name'] = '' # we'd have to look this up in the REST API, not worth it imo
        search['from_user'] = stream['user']['screen_name']
        search['from_user_id'] = stream['user']['id']
        search['from_user_id_str'] = stream['user']['id_str']
        search['from_user_name'] = stream['user']['name']
        search['iso_language_code'] = stream['user']['lang']
        search['profile_image_url'] = stream['user']['profile_image_url']
        search['profile_image_url_https'] = stream['user']['profile_image_url_https']
        # stuff our app uses
        search['origin'] = 'rest'
        search['airport'] = None

    """ main program loop """
    while True:
        # write vital signs 
        updateVitals(db_status, dbname)

        # query for users -> airports, find cases with more than two airports
        interestingQuery = []
        numPeople = 0
        for row in db_airport_tweets.db.view('Tweet/user_airports', group=True, stale='update_after'):
            (key, value) = (int(row.key), row.value.split(', '))
            numPeople += 1
            if len(value) > 1:
                interestingQuery.append(key)
        print "People: %d" % numPeople
        # if the list of interesting people changed, update the stream
        if tweet_stream == None or interestingPeople != interestingQuery:
            interestingPeople = interestingQuery
            tweet_stream = tweetstream.FilterStream(username, password, follow=interestingPeople)
        print "Interesting people: %s" % len(interestingPeople)

        # pull in 
        try:
            for tweet in tweet_stream:
                # prep data slightly
                tweet = rest2search(tweet)
                tweet['text'] = re.sub(pNewLine, ' ', tweet['text']).encode("utf-8")
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
                # increase tweet counts and save
                numTweets += 1
                if tweet['geo'] != None:
                    numGeoTweets += 1
                else:
                    numNonGeoTweets += 1
                db_airport_tweets.save(tweet)
        except (tweetstream.ConnectionError, tweetstream.AuthenticationError) as e:
            print "Encountered issue establishing stream.\n%s" % e
            print "Sleeping for %s seconds..." % pause_time
            time.sleep(pause_time)
            # reset the stream completely
            tweet_stream = None
            interestingPeople = []
        except KeyError as e:
            print "%s" % e
            continue