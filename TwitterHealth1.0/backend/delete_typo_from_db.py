"""
deletes a specified day (year month-1 day) from couch
"""

import couchdb
import datetime
import json
import sys

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def deleteDocs(db):
    badTweets = db.view('Tweet/live_classified')
    print 'Found %d tweets' % len(badTweets)
    numTweets = 0
    for row in badTweets:
        doc = db[row.id]
        if 'live_classiffied' in doc:
            print 'Deleting: %s' % doc
            db.delete(doc)
            numTweets += 1
        else:
            print 'WRONG: %s' % doc
    print '%d tweets deleted from %s' % (numTweets, db)

if __name__ == '__main__':
    dbName = sys.argv[1]
    couch = couchdb.Server('http://166.78.236.179:5984/')
    db = couch[dbName]
    deleteDocs(db)
