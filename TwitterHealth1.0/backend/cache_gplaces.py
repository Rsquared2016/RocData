"""
Read a given type of place (eg GYM, PARK) in NYC and store them in couch
using https://github.com/slimkrazy/python-google-places

The db table's name is based on the place type you choose.

EXAMPLES:
python cache_gplaces.py GYM
python cache_gplaces.py PARK

"""

from googleplaces import GooglePlaces, types
import couchdb
import numpy
import sys
import time
from utils import calcDistanceOptimized

# https://developers.google.com/maps/documentation/places/supported_types
pType = sys.argv[1]


# adam's google places API key
# you can generate your own at https://code.google.com/apis/console/
YOUR_API_KEY = 'AIzaSyAvovlIjcNHXHlUdZqmLk0e_7Y3lUUPxjs'

if pType == "PARK":
    pTypes = [types.TYPE_PARK,types.TYPE_NATURAL_FEATURE]
elif pType == "GYM":
    pTypes = [types.TYPE_GYM]
elif pType == "BAR":
    pTypes = [types.TYPE_BAR, types.TYPE_NIGHT_CLUB]
elif pType == "PUBLIC_TRANSIT":
    pTypes = [types.TYPE_BUS_STATION, types.TYPE_TRAIN_STATION, types.TYPE_SUBWAY_STATION ]
elif pType == "RESTAURANT":
    pTypes = [types.TYPE_RESTAURANT]
else:
    print 'Unrecognized place type %s\nPlease select from {PARK, GYM, PUBLIC_TRANSIT, BAR}' % pType
    exit(-1)

""" Instantiate couchdb """
dbName = 'google_places_%s' % pType.lower()
#dbName = 'boston_traffic'
couch = couchdb.Server('http://166.78.236.179:5984/')
couch.resource.credentials = ('admin', 'admin')
try:
    db = couch.create(dbName) # newly created
except couchdb.http.PreconditionFailed:
    db = couch[dbName]

# NYC
NW = (40.930, -74.206)
NE = (40.924, -73.556)
SW = (40.573, -74.209)
SE = (40.583, -73.567)

# Boston
# NW = (42.426, -71.224)
# NE = (42.416, -70.948)
# SW = (42.266, -71.239)
# SE = (42.250, -70.944)

minLat = min(SW[0], SE[0])
maxLat = max(NW[0], NE[0])
minLon = min(NW[1], SW[1])
maxLon = min(NE[1], SE[1])
#numCellsOneSide = 30 # this way, we stay under the 1K query limit 30^2<1K
numCellsOneSide = 50

offsetMetersPerCell = numpy.mean([calcDistanceOptimized(NW[0], NW[1], SW[0], SW[1]),
                    calcDistanceOptimized(NW[0], NW[1], NE[0], NE[1])]) / numCellsOneSide
print 'Resolution: %f meters.' % offsetMetersPerCell

# Perform grid search over NYC area.
# Google Places does not allow pagination, it only returns up to 20 places.
for lat in numpy.linspace(minLat, maxLat, numCellsOneSide):
    for lon in numpy.linspace(minLon, maxLon, numCellsOneSide):
        while True:
            try:
                query_result = GooglePlaces(YOUR_API_KEY).query(\
                    location='%f,%f' % (lat, lon),\
                    radius=round(offsetMetersPerCell)+100,\
                    types=pTypes,\
                    sensor='false')
                break
            except:
                print 'Error caught, sleeping...'
                time.sleep(3700)

        #if query_result.has_attributions:
            #print query_result.html_attributions

        ids = set()

        for place in query_result.places:
            json = {}
            # Returned places from a query are place summaries.
            json['name'] = place.name
            json['geo_location'] = place.geo_location
            json['id'] = place.id
            json['reference'] = place.reference
            json['vicinity'] = place.vicinity
            json['rating'] = place.rating
            json['icon'] = place.icon
            json['types'] = place.types

            # skip duplicate places
            if place.id in ids:
                print 'Skipping duplicate place: %s (%s)' % (place.name, place.id)
                continue
            ids.add(place.id)

            # unsupported by the python wrapper, but may be useful for us:
            # json['geometry'] = place.geometry
            # json['events'] = place.events

            for (key, value) in sorted(json.items()):
                try:
                    print key, ':', value
                except:
                    pass
            (id, rev) = db.save(json)
            print
            continue

            # The following method has to make a further API call.
            place.get_details()
            # Referencing any of the attributes below, prior to making a call to
            # get_details() will raise a googleplaces.GooglePlacesAttributeError.
            print place.details # A dict matching the JSON response from Google.
            print place.local_phone_number
            print place.formatted_address
            print place.international_phone_number
            print place.website
            print place.url
