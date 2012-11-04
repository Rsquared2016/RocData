import couchdb
import sys

dbName = sys.argv[1]
fileName = sys.argv[2]
#filehandle = open(fileName, 'w')
filehandleGPS = open(fileName, 'w')
""" Instantiate couchdb """
couch = couchdb.Server('http://health.scenedipity.com:5984/')
db = couch[dbName]
for id in db:
        #filehandle.write("%s\n" % str(db[id]))
        try:
                filehandleGPS.write('%f,\t%f\n' % (db[id]['geo_location']['lat'], db[id]['geo_location']['lng']))
        except KeyError:
                print '"geo_location" KeyError: %s' % db[id]
                pass
#filehandle.close()
filehandleGPS.close()
