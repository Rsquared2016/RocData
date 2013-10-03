import sys
from geopy import geocoders
g = geocoders.Google()

string = sys.argv[1]

#place, (lat, lon) = g.geocode("Bronx, NY", exactly_one=False)[0]
place, (lat, lon) = g.geocode(string, exactly_one=False)[0]

print "%s: %.5f, %.5f" % (place, lat, lon)

