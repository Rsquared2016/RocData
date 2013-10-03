import tweetstream
import couchdb
import json
import signal
import sys
import time

class Area:
    def __init__(self, name, latSW, lonSW, latNE, lonNE):
        self.name = name
        self.latSW = latSW
        self.lonSW = lonSW
        self.latNE = latNE
        self.lonNE = lonNE
    def __str__(self):
        return 'Area "%s": SWcorner: [%f, %f], NEcorner: [%f, %f]' % (self.name, self.latSW, self.lonSW, self.latNE, self.lonNE)

# Catch ctrl+C
def signal_handler(signal, frame):
    print 'Terminating'
    print "Tweets logged: %d" % stream.count
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


## --------------------------------------------------------------------------------

username = 'corporaMine'
password = 'tw1tterhea1th'

## --------------------------------------------------------------------------------

# Instantiate couchdb
dbName = sys.argv[1]
couch = couchdb.Server('http://166.78.236.179:5984/')
try:
        db = couch.create(dbName) # newly created
except couchdb.http.PreconditionFailed:
        db = couch[dbName]
        
# Read geo area data
input = open('geo-areas.txt', 'r')
name2a = {}
for line in input:
    if line[0] == '#':
        continue
    columns = line.split()
    if len(columns) != 5:
        print 'Error on line: %s' % line
        continue
    name = columns[0]
    latSW = float(columns[1])
    lonSW = float(columns[2])
    latNE = float(columns[3])
    lonNE = float(columns[4])
    name2a[name] = Area(name, latSW, lonSW, latNE, lonNE)
input.close()

locations = []
for area in name2a.values():
    print area
    locations.append('%f,%f' % (area.lonSW, area.latSW))
    locations.append('%f,%f' % (area.lonNE, area.latNE))   
print "Areas = %s" % locations

stream = tweetstream.FilterStream(username, password, follow=None, locations=locations, track=None, catchup=None, url=None)

while True:
    try:
        for tweet in stream:
            (id, rev) = db.save(tweet)
    except:
        time.sleep(60)
        stream = tweetstream.FilterStream(username, password, follow=None, locations=locations, track=None, catchup=None, url=None)
        pass
        
        
