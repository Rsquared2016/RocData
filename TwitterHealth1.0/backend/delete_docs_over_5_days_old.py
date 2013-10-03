"""
deletes tweets that are more than 5 days old with respect to current time on the server
"""

import couchdb
import datetime
import json
import sys

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def deleteDocs(db):
    print 'Loading old tweets ...'
    oldTweets = db.view('Tweet/by_day_older_five_days')
    print 'Found %d tweets' % len(oldTweets)
    numTweets = 0
    for row in oldTweets:
        doc = db[row.id]
        print 'Deleting: %s' % doc['created_at']
        db.delete(doc)
        numTweets += 1
    print '%d tweets deleted from %s' % (numTweets, db)

if __name__ == '__main__':
    dbName = sys.argv[1]
    couch = couchdb.Server('http://166.78.236.179:5984/')
    couch.resource.credentials = ('admin', 'admin')
    db = couch[dbName]
    deleteDocs(db)
