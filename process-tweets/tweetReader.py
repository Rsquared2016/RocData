from Tweet import *
import re
import simplejson as json
from datetime import datetime

class tweetReader:

    def __init__(self, filename):
        self.GPS = []
        self.duplicates = 0
        self.tweets = 0
        self.GPStweets = 0
        self.problems = 0
        self.f = open(filename, 'r')
        self.rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
        self.rexCreated = re.compile('([A-Z][a-z][a-z]), ([0-9][0-9]) (...) ([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})')
	self.months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    def getNextTweet(self):
        tweet = Tweet()
        line = self.f.readline()
        if line == "":
            self.f.close()
            return None
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            print "Problematic JSON string:"
            print line
            self.problems += 1
            return None

       
        # Extract GPS: try 'geo' tag, fallback to 'location' tag
        if o['geo'] != None:
            self.GPStweets += 1
            (tweet.lat, tweet.lon) = o['geo']['coordinates']
        else:
            try:
                tweet.location = o['location']
                match = self.rexLatLon.search(tweet.location)
                if bool(match):
                    self.GPStweets += 1
                    (tweet.lat, tweet.lon) = float(match.group('lat')), float(match.group('lon'))
            except KeyError:
                print "Location Key Error"
                pass
                #raise

        self.tweets += 1
        if self.tweets%100000 == 0:
            print "Tweets so far: " + str(self.tweets)

        #tweet.WRONGuserID = o['from_user_id']
        tweet.userName = o['from_user']
        tweet.text = o['text'].encode("utf-8")
        tweet.createdAt = o['created_at']
        tweet.profile_image = o['profile_image_url']
        tweet.msgID = int(o['id'])
        tweet.json = line.strip()
	datematch = self.rexCreated.match(o['created_at']).groups()
	tweet.datetime = datetime( int(datematch[3]), 
		self.months.index(datematch[2]), 
		int(datematch[1]), 
		int(datematch[4]), 
		int(datematch[5]), 
		int(datematch[6]))
        return (tweet, line)

        
    def printInfo(self):
        print "_________________________________________________"
        print "Tweets: %d" % self.tweets
        print "Problematic JSON strings: %d" % self.problems
        print "GPS locations: %d (rate: %.2f%%)" % (self.GPStweets, self.GPStweets/float(self.tweets)*100)


    def getGPSlist(self):
        return self.GPS

