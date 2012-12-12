
import couchdb
import math
import sys

def calcDistance(lat1, lon1, lat2, lon2):                
    rad = 0.017453292519943
    yDistance = (lat2 - lat1) * 60.00721
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * 30.053965
    distance = math.sqrt( yDistance*yDistance + xDistance*xDistance )
    return round(distance * 1852.00088832)

def find_closest_city(doc):
    if len(doc['geo']['coordinates']) == 2:
        closestCityID = ""
        minDist = 999999999;
        for center in centers:
            dist = calcDistance(doc['geo']['coordinates'][0], doc['geo']['coordinates'][1], center[0], center[1]);
            if dist < minDist:
                minDist = dist
                closestCityID = center[2]
        return closestCityID
    else:
        return None

centers = [
    [42.3644,-71.059,"BOS"],
    [40.716667,-74.00,"NYC"],
    [33.995,-118.063,"LA"],
    [51.514,-0.122,"LON"],
    [47.577,-122.229,"SEA"],
    [37.566,-122.327,"SF"]
]

couch = couchdb.Server('http://fount.in:5984')
couch_dev = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
couch_dev.resource.credentials = ('admin', 'admin')
db = couch['m']
db_dev = couch_dev['m_toy']
numTweets = 0
results = db.view('Tweet/by_day_all_geo',
    reduce = False,
    include_docs = True,
    startkey = [2012, 11, 3],
    endkey = [2012, 11, 9])
print "Grabbing NYC and SF..."
for row in results:
    doc = row.doc
    closest = find_closest_city(doc)
    if closest == "NYC" or closest == "SF":
        try:
            db_dev.save(doc, batch = 'ok')
            numTweets += 1
            if numTweets % 50 == 0:
                print "%s tweets read." % numTweets
        except couchdb.http.ResourceConflict:
            continue
print "%s tweets read. Done." % numTweets
    