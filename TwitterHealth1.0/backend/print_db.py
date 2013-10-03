import couchdb
import sys

dbName = sys.argv[1]

""" Instantiate couchdb """
couch = couchdb.Server('http://166.78.236.179:5984/')
db = couch[dbName]

for id in db:
    o = db[id]
    print o


#couch.delete('adam_test')
