from pykml import parser
from lxml import etree
from utils import *
import os
import cPickle as pickle
import sys

def parseKML(xmlFile):
    """"""
    NYC_ZIPs = pickle.load(open('NYC_ZIPs.pickle', 'rb')) #set
    print len(NYC_ZIPs)
    events = ("start", "end")
    context = etree.iterparse(xmlFile, events=events)
    lastPlacemark = None
    for action, elem in context:
        print action, elem.tag
        if elem.tag[-9:] == 'Placemark' and action == 'start':
            print lastPlacemark
            lastPlacemark = elem
            print lastPlacemark.tag

        tag = elem.tag[-11:]
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        
        if tag[-4:] == "name" and action == 'end':
            try:
                zip_code = int(text)
            except ValueError:
                continue
            if zip_code in NYC_ZIPs:
                continue
            print tag[-4:] + " => " + text
            print 'removing %s' % lastPlacemark.tag
            lastPlacemark.clear()

    out = etree.tostring(context.root, pretty_print=True)
    out = out.replace('<Placemark/>', '')
    #print out

    fout = open('%s_filtered.kml' % os.path.splitext(kml_file)[-2], 'w')
    fout.write(out)
    fout.close()
    
if __name__ == "__main__":
    kml_file = sys.argv[1]
    parseKML(kml_file)
        
