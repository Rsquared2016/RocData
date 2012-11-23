
import couchdb
import sys

couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch['airport_tweets']
results = db.view('Streamed/all', include_docs=True)
for row in results:
    doc = row.doc
    db.delete(doc)
    