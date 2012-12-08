# Lat Long - UTM, UTM - Lat Long conversions

from math import pi, sin, cos, tan, sqrt
from datetime import datetime, date, timedelta
from time import mktime
import math



def calcDistance(lat1, lon1, lat2, lon2):                      
    """
    Caclulate distance between two lat lons in meters
    """
    nauticalMilePerLat = 60.00721
    nauticalMilePerLongitude = 60.10793
    rad = math.pi / 180.0
    milesPerNauticalMile = 1.15078
    
    yDistance = (lat2 - lat1) * nauticalMilePerLat
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)

    distance = math.sqrt( yDistance**2 + xDistance**2 )

    return distance * milesPerNauticalMile * 1609.344

def calcDistanceOptimized(lat1, lon1, lat2, lon2):                      
    """
    Caclulate distance between two lat lons in meters
    """
    rad = 0.017453292519943
    yDistance = (lat2 - lat1) * 60.00721
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * 30.053965
    distance = math.sqrt( yDistance**2 + xDistance**2 )
    return distance * 1852.00088832

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Folder>
    <GroundOverlay>
      <Icon>
        <href>%s</href>
      </Icon>
      <LatLonBox>
        <north>%2.16f</north>
        <south>%2.16f</south>
        <east>%2.16f</east>
        <west>%2.16f</west>
        <rotation>0</rotation>
      </LatLonBox>
    </GroundOverlay>
  </Folder>
</kml>"""

def saveKML(kmlFile):
        """ 
        Saves a KML template to use with google earth.  Assumes x/y coordinates 
        are lat/long, and creates an overlay to display the heatmap within Google
        Earth.

        kmlFile ->  output filename for the KML.
        """

        tilePath = os.path.basename('map-NYC_heatmap.png')
        north = topLeftLat
        south = bottomRightLat
        east = topLeftLon
        west = bottomRightLon
        
        bytes = KML % (tilePath, north, south, east, west)
        file(kmlFile, "w").write(bytes)

def getTime2012(s):
        # get normal time and UNIX time from a string       
        t = datetime.strptime(s, "%a %b %d %H:%M:%S +0000 %Y")
        #t = t+timedelta(hours=-6)
        UNIXt = int(mktime(t.timetuple())+1e-6*t.microsecond)
        return (t, UNIXt)
        
def getTime(s):
        # get normal time and UNIX time from a string       
        t = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S +0000")
        #t = t+timedelta(hours=-6)
        UNIXt = int(mktime(t.timetuple())+1e-6*t.microsecond)
        return (t, UNIXt)

def getUnmodTime(s):
        # get normal time and UNIX time from a string       
        t = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S -0006")
        UNIXt = int(mktime(t.timetuple())+1e-6*t.microsecond)
        return (t, UNIXt)


#LatLong- UTM conversion..h
#definitions for lat/long to UTM and UTM to lat/lng conversions
#include <string.h>

_deg2rad = pi / 180.0
_rad2deg = 180.0 / pi

_EquatorialRadius = 2
_eccentricitySquared = 3

_ellipsoid = [
#  id, Ellipsoid name, Equatorial Radius, square of eccentricity	
# first once is a placeholder only, To allow array indices to match id numbers
	[ -1, "Placeholder", 0, 0],
	[ 1, "Airy", 6377563, 0.00667054],
	[ 2, "Australian National", 6378160, 0.006694542],
	[ 3, "Bessel 1841", 6377397, 0.006674372],
	[ 4, "Bessel 1841 (Nambia] ", 6377484, 0.006674372],
	[ 5, "Clarke 1866", 6378206, 0.006768658],
	[ 6, "Clarke 1880", 6378249, 0.006803511],
	[ 7, "Everest", 6377276, 0.006637847],
	[ 8, "Fischer 1960 (Mercury] ", 6378166, 0.006693422],
	[ 9, "Fischer 1968", 6378150, 0.006693422],
	[ 10, "GRS 1967", 6378160, 0.006694605],
	[ 11, "GRS 1980", 6378137, 0.00669438],
	[ 12, "Helmert 1906", 6378200, 0.006693422],
	[ 13, "Hough", 6378270, 0.00672267],
	[ 14, "International", 6378388, 0.00672267],
	[ 15, "Krassovsky", 6378245, 0.006693422],
	[ 16, "Modified Airy", 6377340, 0.00667054],
	[ 17, "Modified Everest", 6377304, 0.006637847],
	[ 18, "Modified Fischer 1960", 6378155, 0.006693422],
	[ 19, "South American 1969", 6378160, 0.006694542],
	[ 20, "WGS 60", 6378165, 0.006693422],
	[ 21, "WGS 66", 6378145, 0.006694542],
	[ 22, "WGS-72", 6378135, 0.006694318],
	[ 23, "WGS-84", 6378137, 0.00669438]
]

#Reference ellipsoids derived from Peter H. Dana's website- 
#http://www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
#Department of Geography, University of Texas at Austin
#Internet: pdana@mail.utexas.edu
#3/22/95

#Source
#Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to Department of Defense World Geodetic System
#1984 Technical Report. Part I and II. Washington, DC: Defense Mapping Agency

#def LLtoUTM(int ReferenceEllipsoid, const double Lat, const double Long, 
#			 double &UTMNorthing, double &UTMEasting, char* UTMZone)

def LLtoUTM(lat, lon):
    return (LLtoUTMSpecific(23, lat, lon)[1],  LLtoUTMSpecific(23, lat, lon)[2]) 
    
def LLtoUTMSpecific(ReferenceEllipsoid, Lat, Long):
#converts lat/long to UTM coords.  Equations from USGS Bulletin 1532 
#East Longitudes are positive, West longitudes are negative. 
#North latitudes are positive, South latitudes are negative
#Lat and Long are in decimal degrees
#Written by Chuck Gantz- chuck.gantz@globalstar.com

    a = _ellipsoid[ReferenceEllipsoid][_EquatorialRadius]
    eccSquared = _ellipsoid[ReferenceEllipsoid][_eccentricitySquared]
    k0 = 0.9996

#Make sure the longitude is between -180.00 .. 179.9
    LongTemp = (Long+180)-int((Long+180)/360)*360-180 # -180.00 .. 179.9

    LatRad = Lat*_deg2rad
    LongRad = LongTemp*_deg2rad

    ZoneNumber = int((LongTemp + 180)/6) + 1
  
    if Lat >= 56.0 and Lat < 64.0 and LongTemp >= 3.0 and LongTemp < 12.0:
        ZoneNumber = 32

    # Special zones for Svalbard
    if Lat >= 72.0 and Lat < 84.0:
        if  LongTemp >= 0.0  and LongTemp <  9.0:ZoneNumber = 31
        elif LongTemp >= 9.0  and LongTemp < 21.0: ZoneNumber = 33
        elif LongTemp >= 21.0 and LongTemp < 33.0: ZoneNumber = 35
        elif LongTemp >= 33.0 and LongTemp < 42.0: ZoneNumber = 37

    LongOrigin = (ZoneNumber - 1)*6 - 180 + 3 #+3 puts origin in middle of zone
    LongOriginRad = LongOrigin * _deg2rad

    #compute the UTM Zone from the latitude and longitude
    UTMZone = "%d%c" % (ZoneNumber, _UTMLetterDesignator(Lat))

    eccPrimeSquared = (eccSquared)/(1-eccSquared)
    N = a/sqrt(1-eccSquared*sin(LatRad)*sin(LatRad))
    T = tan(LatRad)*tan(LatRad)
    C = eccPrimeSquared*cos(LatRad)*cos(LatRad)
    A = cos(LatRad)*(LongRad-LongOriginRad)

    M = a*((1
            - eccSquared/4
            - 3*eccSquared*eccSquared/64
            - 5*eccSquared*eccSquared*eccSquared/256)*LatRad 
           - (3*eccSquared/8
              + 3*eccSquared*eccSquared/32
              + 45*eccSquared*eccSquared*eccSquared/1024)*sin(2*LatRad)
           + (15*eccSquared*eccSquared/256 + 45*eccSquared*eccSquared*eccSquared/1024)*sin(4*LatRad) 
           - (35*eccSquared*eccSquared*eccSquared/3072)*sin(6*LatRad))
    
    UTMEasting = (k0*N*(A+(1-T+C)*A*A*A/6
                        + (5-18*T+T*T+72*C-58*eccPrimeSquared)*A*A*A*A*A/120)
                  + 500000.0)

    UTMNorthing = (k0*(M+N*tan(LatRad)*(A*A/2+(5-T+9*C+4*C*C)*A*A*A*A/24
                                        + (61
                                           -58*T
                                           +T*T
                                           +600*C
                                           -330*eccPrimeSquared)*A*A*A*A*A*A/720)))

    if Lat < 0:
        UTMNorthing = UTMNorthing + 10000000.0; #10000000 meter offset for southern hemisphere
    return (UTMZone, UTMEasting, UTMNorthing)


def _UTMLetterDesignator(Lat):
#This routine determines the correct UTM letter designator for the given latitude
#returns 'Z' if latitude is outside the UTM limits of 84N to 80S
#Written by Chuck Gantz- chuck.gantz@globalstar.com

    if 84 >= Lat and Lat >= 72: return 'X'
    elif 72 > Lat and Lat >= 64: return 'W'
    elif 64 > Lat and Lat >= 56: return 'V'
    elif 56 > Lat and Lat >= 48: return 'U'
    elif 48 > Lat and Lat >= 40: return 'T'
    elif 40 > Lat and Lat >= 32: return 'S'
    elif 32 > Lat and Lat >= 24: return 'R'
    elif 24 > Lat and Lat >= 16: return 'Q'
    elif 16 > Lat and Lat >= 8: return 'P'
    elif  8 > Lat and Lat >= 0: return 'N'
    elif  0 > Lat and Lat >= -8: return 'M'
    elif -8> Lat and Lat >= -16: return 'L'
    elif -16 > Lat and Lat >= -24: return 'K'
    elif -24 > Lat and Lat >= -32: return 'J'
    elif -32 > Lat and Lat >= -40: return 'H'
    elif -40 > Lat and Lat >= -48: return 'G'
    elif -48 > Lat and Lat >= -56: return 'F'
    elif -56 > Lat and Lat >= -64: return 'E'
    elif -64 > Lat and Lat >= -72: return 'D'
    elif -72 > Lat and Lat >= -80: return 'C'
    else: return 'Z'	# if the Latitude is outside the UTM limits


def addEndsToTraceGPS(l1, tstart, tend):
    tmp = l1[:]
    n1 = len(l1)
    for i in xrange(0,n1-1):
        (t1,lat1,lon1) = l1[i]
        (t2,lat2,lon2) = l1[i+1]
        tmp[i] = (t1,t2,lat1,lon1)

    if l1[-1][0] == tend:
        # this is the longer sequence
        tmp.pop(len(tmp)-1)
    else:
        (t1,lat1,lon1) = l1[-1]
        tmp[-1] = (t1,tend,lat1,lon1) 
    return tmp

def addEndsToTraceDiscrete(l1, tstart, tend):
    tmp = l1[:]
    n1 = len(l1)
    for i in xrange(0,n1-1):
        (t1,cell1) = l1[i]
        (t2,cell2) = l1[i+1]
        tmp[i] = (t1,t2,cell1)

    if l1[-1][0] == tend:
        # this is the longer sequence
        tmp.pop(len(tmp)-1)
    else:
        (t1,cell1) = l1[-1]
        tmp[-1] = (t1,tend,cell1) 
    return tmp

# return continuous colocation score given two GPS traces
def calculateCoLocationsGPS(l1, l2):
    # l1 = [ (UNIXt,lat,lon), ... ]
    tstart = min(l1[0][0],l2[0][0])
    tend = max(l2[-1][0],l2[-1][0])
    
    # add end time points
    l1 = addEndsToTraceGPS(l1, tstart, tend)
    l2 = addEndsToTraceGPS(l2, tstart, tend)
    #print l1
    #print l2
    n1 = len(l1)
    n2 = len(l2)
    
    score = 0
    for i in xrange(n1):
        (t1a,t1b,lat1,lon1) = l1[i]
        for j in xrange(n2):
            (t2a,t2b,lat2,lon2) = l2[j]
            if t1a <= t2b and t1b >= t2a:
                #print t1a, ",", t1b, "-", t2a, ",", t2b
                d = calcDistanceOptimized(lat1,lon1,lat2,lon2)
                if d <= 500:
                    if d == 0:
                        d = 0.1
                    timeOverlap = min(t1b-t2a, t2b-t2a)
                    #score +=1
                    score += timeOverlap / float(d) / 60.0
    return score

# return a list of cell_ids within which user1 and user2 check-in
# within timeThreshold (in hours)
def calculateCoLocationsDiscrete_weird(l1, l2, timeThreshold):
    # l1 = [ (UNIXt, cell_id), ... ]
    tstart = min(l1[0][0],l2[0][0])
    tend = max(l2[-1][0],l2[-1][0])

    # convert from hours to seconds
    timeThreshold = timeThreshold*3600
    
    # add end time points
    l1 = addEndsToTraceDiscrete(l1, tstart, tend)
    l2 = addEndsToTraceDiscrete(l2, tstart, tend)

    n1 = len(l1)
    n2 = len(l2)
    
    score = 0
    cells = []
    for i in xrange(n1):
        (t1a,t1b,cell1) = l1[i]
        for j in xrange(n2):
            (t2a,t2b,cell2) = l2[j]
            if t1a <= t2b and t1b >= t2a:
                timeOverlap = min(t1b-t2a, t2b-t2a)
                if cell1 == cell2 and timeOverlap <= timeThreshold:
                    score +=1
                    cells.append(cell1)
    return cells

# return a list of cell_ids within which user1 and user2 check-in
# within timeThreshold (in hours)
def calculateCoLocationsDiscrete(l1, l2, timeThreshold):
    # l1 = [ (UNIXt, cell_id), ... ]
    tstart = min(l1[0][0],l2[0][0])
    tend = max(l2[-1][0],l2[-1][0])

    # convert from hours to seconds
    timeThreshold = timeThreshold*3600
    
    n1 = len(l1)
    n2 = len(l2)
    
    score = 0
    cells = []
    for (t1, cell1) in l1:
        for (t2, cell2) in l2:
            if t2 > t1+timeThreshold:
                break
            if abs(t1-t2) <= timeThreshold and cell1 == cell2:
                score +=1
                cells.append(cell1)
    return cells

if __name__ == '__main__':
    l1 = [ (1,5), (5,4), (7,3), (10,5) ]
    l2 = [ (1,5), (6,5), (7,3), (9,5) ]
    print calculateCoLocationsDiscrete(l1, l2, 5/3600.0)
