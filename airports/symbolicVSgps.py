
## scans a log file that contains public timeline tweets (with associated user info)
## and extracts all GPS-tagged tweets 

import re
import sys
from operator import itemgetter
import simplejson as json

class readGPStweets:

    def __init__(self, filename):
        self.GPS = []
        self.userIDs = {}
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

        try:
            location = o['location']
        except KeyError:
            print "Location Key Error"
            return "Error"
            #raise

        self.tweets += 1
        #if self.tweets%50000 == 0:
        #    print "Tweets so far: " + str(self.tweets)

        #userID = o['from_user_id']
        #userName = o['from_user']
        #self.userIDs[userID] = userName
        
        #createdAt = o['created_at']
        return location.strip().lower()
    
        ## match = self.rexLatLon.search(location)

        ## if bool(match):
        ##     #print location
        ##     #print match.group('lat'), "\t", match.group('lon')
        ##     self.GPStweets += 1
        ##     pair = float(match.group('lat')), float(match.group('lon'))
        ##     return (pair, userID, createdAt)

        
    def printInfo(self):
        print "_________________________________________________"
        print "Tweets: %s" % self.tweets
        print "Duplicate tweets (redundancy removed): %s" % self.duplicates
        print "Problematic JSON strings: %s" % self.problems
        #print "GPS locations: %s (rate: %s%%)" % (self.GPStweets, self.GPStweets/float(self.tweets)*100)


    def getGPSlist(self):
        return self.GPS

r = readGPStweets(sys.argv[1])
#r = readGPStweets("log-geo-area_NYC_GPS.txt_sorted.txt")

location_histogram = {}
loc = r.getNextGPS()
while loc != None:
    try:
        location_histogram[loc] = location_histogram[loc] + 1
    except KeyError:
        location_histogram[loc] = 1
    loc = r.getNextGPS()


for w in sorted(location_histogram.items(), key=itemgetter(1), reverse=False):
      print "%s\t%s" % (unicode(w[0]).encode("utf-8"), unicode(w[1]).encode("utf-8"))

#r.printInfo()

#print ID_count
