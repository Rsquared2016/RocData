from pykml import parser
from lxml import etree
from utils import *
import os
import sys

def parseKML(xmlFile):
    """"""

    NYClat = 40.7319
    NYClon = -73.996
    
    events = ("start", "end")
    context = etree.iterparse(xmlFile, events=events)
    lastPlacemark = None
    for action, elem in context:
        #print action, elem.tag
        if elem.tag[-9:] == 'Placemark' and action == 'start':
            lastPlacemark = elem
      
        tag = elem.tag[-11:]
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        
        if tag == "coordinates" and action == 'end':
            #print tag + " => " + text
            try:
                (lon, lat, void) = text.split(',')
            except ValueError:
                continue
            lat = float(lat)
            lon = float(lon)
            if calcDistanceOptimized(lat, lon, NYClat, NYClon) > 60000:
                lastPlacemark.clear()
                #print 'removing %s' % lastPlacemark.tag

    out = etree.tostring(context.root, pretty_print=True)
    out = out.replace('<Placemark/>', '')
    print out

    fout = open('%s_filtered.kml' % os.path.splitext(kml_file)[-2], 'w')
    fout.write(out)
    fout.close()
    
if __name__ == "__main__":
    kml_file = sys.argv[1]
    parseKML(kml_file)
        
