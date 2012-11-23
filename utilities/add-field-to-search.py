
import couchdb
import sys

couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch['airport_tweets']
map_fun = '''function(doc) {
    if(!doc.origin)
        emit(doc._id, doc.text);
}'''
results = db.query(map_fun, include_docs=True)
for row in results:
    doc = row.doc
    doc['origin'] = 'search'
    db.save(doc)
    