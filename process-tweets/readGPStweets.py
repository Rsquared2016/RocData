
## scans a log file that contains public timeline tweets (with associated user info)
## and extracts all GPS-tagged tweets 

import re
import simplejson as json

class readGPStweets:

    def __init__(self, filename):
        self.GPS = []
        self.msgids = {}
        self.duplicates = 0
        self.tweets = 0
        self.GPStweets = 0
        self.problems = 0

        self.f = open(filename, 'r')
        
        self.rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')


    def getNextGPS(self):
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
            return ()

        msgid = int(o['id'])
        if msgid in self.msgids:
            self.duplicates += 1
            return ()
        else:
            self.msgids[msgid] = True

        try:
            location = o['location']
        except KeyError:
            print "Location Key Error"
            raise

        self.tweets += 1
        #if tweets%5000 == 0:
        #    print "Tweets so far: " + str(tweets)

        userID = o['from_user_id']
        userName = o['from_user']
        createdAt = o['created_at']
        match = self.rexLatLon.search(location)

        if bool(match):
            #print location
            #print match.group('lat'), "\t", match.group('lon')
            self.GPStweets += 1
            pair = float(match.group('lat')), float(match.group('lon'))
            return (pair, userName, createdAt)

        
    def printInfo(self):
        print "_________________________________________________"
        print "Tweets: %s" % self.tweets
        print "Duplicate tweets (redundancy removed): %s" % self.duplicates
        print "Problematic JSON strings: %s" % self.problems
        print "GPS locations: %s (rate: %s%%)" % (self.GPStweets, self.GPStweets/float(self.tweets)*100)


    def getGPSlist(self):
        return self.GPS


    
