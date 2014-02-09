from Tweet import *
import re
import simplejson as json
from datetime import datetime
import sys

class tweetReader:

    def __init__(self, filename):
        self.GPS = []
        self.duplicates = 0
        self.tweets = 0
        self.GPStweets = 0
        self.problems = 0
        self.f = open(filename, 'r')
        self.rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
        
    def getNextTweet(self):
        tweet = Tweet()
        line = self.f.readline()
        if line == "":
        #    print "Missing line:" 
            print self.tweets
            self.f.close()
            return None
        try:
            o = json.loads(line)
            #print o['doc']
            #o = json.loads(o['doc'])
        except json.decoder.JSONDecodeError as e:
            print "Problematic JSON string:"
            print line
            print e.args
            self.problems += 1
            return None

       
        # Extract GPS: try 'geo' tag, fallback to 'location' tag
        try:
            if o['doc']['geo'] != None:
                (tweet.lat, tweet.lon) = o['doc']['geo']['coordinates']
                self.GPStweets += 1
            else:
                try:
                    tweet.location = o['doc']['location']
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
            tweet.userName = o['doc']['from_user']
            tweet.text = o['doc']['text'].encode("utf-8")
            tweet.createdAt = o['doc']['created_at']
            tweet.profile_image = o['doc']['profile_image_url']
            tweet.msgID = int(o['doc']['id'])
            #tweet.sentiment = float(o['doc']['sentiment'])
            #tweet.json = line.strip()
            tweet.datetime = datetime.strptime(tweet.createdAt, "%a, %d %b %Y %H:%M:%S +0000")
            return (tweet, line)
        except KeyError:
            print "KeyError:"
            print line # o
            print "TWEETS"
            print self.tweets
            return "Err"
  
        
    def printInfo(self):
        print "_________________________________________________"
        print "Tweets: %d" % self.tweets
        print "Problematic JSON strings: %d" % self.problems
        print "GPS locations: %d (rate: %.2f%%)" % (self.GPStweets, self.GPStweets/float(self.tweets)*100)


    def getGPSlist(self):
        return self.GPS

