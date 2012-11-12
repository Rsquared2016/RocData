import traceback

class Airport:
    def __init__(self, name, code, lat, lon):
        self.name = name
        self.code = code
        self.lat = lat
        self.lon = lon
    def __str__(self):
        return 'Airport %s (%s): [%f, %f]' % (code, name, lat, lon)

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
from twython import Twython
import time
import json
import signal
import sys
import httplib

# Catch ctrl+C
def signal_handler(signal, frame):
        print 'Terminating, flushing file %s' % fileName
        log.close()
        print "Tweets logged: %d" % numTweets
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

""" Instantiate Twython with no Authentication """
twitter = Twython()

#Geo_area = "34.05,-118.25,150km" # Los Angeles
#geo_area = "43.165556,-77.611389,80km" # Rochester, NY
#geo_area = "40.716667,-74.00,100km" # NYC


lastID = []
numTweets = 0
gps = 0
location = 0
numSuccessfulQueries = 0
waitTime = 5 # minutes
pauseTime = float(sys.argv[3]) # minutes

begin = int(sys.argv[1])
end = int(sys.argv[2])
print 'Collecting airports %d through %d' % (begin, end)

for a in range(begin,end+1):
    lastID.append(0)

while True:
    for (i, a) in enumerate(range(begin,end+1)):
        airport = code2a[codes[a]]
        fileName = 'log/log-geo-area_%s.txt' % airport.code
        log = open(fileName, 'a', 0)
        radius = '3km'
        geo_area = '%f,%f,%s' % (airport.lat, airport.lon, radius)
        try:
            search_results = twitter.searchTwitter(q="", rpp="100", lang="en", geocode=geo_area, since_id=str(lastID[i]), result_type="recent")
        #except (ValueError, AttributeError, httplib.BadStatusLine):
        except: # catch all problems
            print 'Error caught, continuing after %d seconds' % (waitTime*60)
            log.close()
            print i, a
            printException()
            time.sleep(waitTime *60)
            twitter = Twython()
            continue
        #print search_results
        try:
            e = search_results['error']
            print 'Error caught: %s' % e
            print 'Waiting for %d minutes' % waitTime
            time.sleep(waitTime * 60)
            log.close()
            continue
        except KeyError:
            numSuccessfulQueries += 1

        for tweet in search_results["results"]:
            numTweets += 1
            if lastID[i] < tweet["id"]: 
                lastID[i] = tweet["id"]
            log.write(json.dumps(tweet))
            log.write('\n')
            if numTweets % 1000 == 0:
                #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                print str(numTweets)+" tweets logged, "+str(location)+" have at least symbolic location info, "+str(gps)+" have specific GPS field filled in."
                #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            try:        
                if  tweet["geo"] != None:
                    gps += 1
                elif  tweet["location"] != None:
                    location += 1
            except KeyError:
                pass

            print '%s: %s' % (airport.code, tweet["text"].encode('utf-8'))
        sys.stdout.flush()
        log.close()
    time.sleep(pauseTime * 60)





