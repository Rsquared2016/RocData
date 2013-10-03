"""
deletes a specified day (year month day) from couch
"""

import couchdb
import datetime
import json
import sys

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def deleteDocs(db, year, month, day):
    print 'Loading tweets for (year=%d month=%d day=%d)' % (year, month-1, day) # couch uses months indexed from 0!
    todayTweets = db.view('Tweet/by_day', key=[year, month-1, day])
    print 'Found %d tweets' % len(todayTweets)
    numTweets = 0
    for row in todayTweets:
        doc = db[row.id]
        print 'Deleting: %s' % doc['created_at']
        db.delete(doc)
        numTweets += 1
    print '%d tweets deleted from %s' % (numTweets, db)

if __name__ == '__main__':
    dbName = sys.argv[1]
    couch = couchdb.Server('http://166.78.236.179:5984/')
    db = couch[dbName]
    deleteDocs(db, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
