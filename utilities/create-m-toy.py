
import couchdb
import sys

couch = couchdb.Server('http://fount.in:5984')
couch_dev = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
couch_dev.resource.credentials = ('admin', 'admin')
db = couch['m']
db_dev = couch_dev['m_toy']
numTweets = 0
results_nyc = db.view('Tweet/by_closest_city_day',
    reduce = False,
    include_docs = True,
    startkey = ["NYC", 2012, 11, 17],
    endkey = ["NYC", 2012, 12, 9])
results_sf = db.view('Tweet/by_closest_city_day',
    reduce = False,
    include_docs = True,
    startkey = ["SF", 2012, 11, 17],
    endkey = ["SF", 2012, 12, 9])
print "Grabbing NYC..."
for row in results_nyc:
    doc = row.doc
    db_dev.save(doc)
    numTweets += 1
    if numTweets % 50 == 0:
        print "%s tweets read." % numTweets
print "Grabbing SF..."
for row in results_sf:
    doc = row.doc
    db_dev.save(doc)
    numTweets += 1
    if numTweets % 50 == 0:
        print "%s tweets read." % numTweets
print "%s tweets read. Done." % numTweets
    