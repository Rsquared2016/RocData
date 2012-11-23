
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
    pause_time = float(sys.argv[1])
    refresh_time = int(sys.argv[2])
    last_time = int(datetime.datetime.utcnow().strftime("%s"))
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
    def updateVitals(db, name, numPeople, numInteresting):
        idFor = '%s (%s) @ %s' % (name + '_interesting', "N/A", ip_addr)
        doc = db.get(idFor)
        try:
            status = {
                '_id': idFor,
                'num_tweets': numTweets,
                'num_geo_tweets': numGeoTweets,
                'num_non_geo_tweets': numNonGeoTweets,
                'num_people': numPeople,
                'num_interesting': numInteresting,
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
        return search

    """ sleep if rate limit is hit """
    def backoff():
        current_time = int(datetime.datetime.utcnow().strftime("%s"))
        current_delta = current_time - last_time
        refresh_delta = refresh_time - current_delta + 1
        print "Sleeping for %s seconds..." % refresh_delta
        time.sleep(refresh_delta)
        # reset the stream completely
        last_time = int(datetime.datetime.utcnow().strftime("%s"))
        interestingPeople = []

    """ main program loop """
    while True:
        # query for users -> airports, find cases with more than two airports
        interestingPeople = []
        numPeople = 0
        for row in db_airport_tweets.db.view('Tweet/user_airports', group=True, stale='update_after'):
            (key, value) = (int(row.key), row.value.split(', '))
            numPeople += 1
            if len(value) > 1:
                interestingPeople.append(key)
        print "People: %d" % numPeople
        print "Interesting people: %s" % len(interestingPeople)

        # pull in "interesting" tweets via the REST API, slowly
        try:
            for uid in interestingPeople:
                # grab user timeline
                tweets = twitter.getUserTimeline(user_id=uid, count=10)
                # check for rate limit, back off if so
                try:
                    response = tweets['error']
                    backoff()
                    continue
                except KeyError:
                    pass

                print "[%s]: %d tweets" % (uid, len(tweets))
                for tweet in tweets:
                    # prep data slightly
                    tweet = rest2search(tweet)
                    tweet['text'] = re.sub(pNewLine, ' ', tweet['text']).encode("utf-8")
                    print "[%s]: says %s" % (uid, tweet['text'])
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
                time.sleep(pause_time)
                # write status if ~60s have elapsed
                current_time = int(datetime.datetime.utcnow().strftime("%s"))
                if current_time - last_time >= 60:
                    updateVitals(db_status, dbname, numPeople, len(interestingPeople))
                # update last_time if ~3600s have elapsed (rate limit)
                if current_time - last_time >= 3600:
                    last_time = int(datetime.datetime.utcnow().strftime("%s"))
        except KeyError as e:
            print "%s" % e
            continue
        except Exception as e:
            print "Uh oh, something bad happened..."
            traceback.print_exc()
            sys.exit()
