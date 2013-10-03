import couchdb

def useThisGeoTweet(tweet, foutKML):
    foutKML.write('<Placemark><name>%s</name><description>%s\n%s</description><styleUrl>#hideLabel</styleUrl>\n' % (tweet['from_user'], tweet['text'].encode("utf-8"), tweet['created_at']))
    foutKML.write('<Point><coordinates>%f,%f,0</coordinates></Point></Placemark>\n' % (tweet['geo']['coordinates'][1], tweet['geo']['coordinates'][0]))


dbName = 'redmond'
foutKML = open("%s_GPS.kml" % dbName, 'w')
foutKML.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n')
foutKML.write('<Style id="hideLabel"><LabelStyle><scale>0</scale></LabelStyle></Style>\n')
couch = couchdb.Server('http://fount.in:5984/')
db = couch[dbName]
allGeoTweets = db.view('Tweet/all', include_docs=True)

for row in allGeoTweets:
    tweet = row.doc
    useThisGeoTweet(tweet, foutKML)

foutKML.write('</Document></kml>')        
foutKML.close()
    
