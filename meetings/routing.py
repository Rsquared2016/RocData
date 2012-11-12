"""
Hypothetical package routing using data from Jan 1 0am to Jan 2 midnight, counting two people "meeting" when they are 100 meters apart within 1 hour at some point.
python -OO routing.py data/rectangle_DateTime_greater_Seattle_2012_January_10K_uniq.txt 2012 1 1 2012 1 3 100 1

"""

import cPickle as pickle
import colorsys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import operator
import os
import random
import rtree
import sys
from datetime import datetime
from pylab import get_cmap
from rtree import index
from Tweet import *
from scipy.io import savemat
from scipy.sparse import csr_matrix
from utils import *

class MyNode:
    def __init__(self, nodeID, tweet):
        self.nodeID = nodeID
        self.dt = tweet.dt        
        self.lat = tweet.lat
        self.lon = tweet.lon

class Cell:
    def __init__(self, id, left, bottom, right, top, num_tweets):        
        self.center_lat = (bottom+top)/2.0
        self.center_lon = (left+right)/2.0
        #self.id = '%f,%f' % (self.center_lat, self.center_lon)
        self.id = id
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.num_tweets = num_tweets

class Ddict(dict):
    def __init__(self, default=None):
        self.default = default

    def __getitem__(self, key):
        if not self.has_key(key):
            self[key] = self.default()
        return dict.__getitem__(self, key)        
        
def fileExists(path):
    try:
       with open(path) as f: return True 
    except IOError as e:
       return False    
       
def updateDic(key, value, d):
    """ Add value to the count in d[key], create this entry as [value] if it doesn't exist """
    try:
         d[key] += value
    except KeyError:
        d[key] = value
                       
def plotGraph(G):
    FIGSIZEX = 50
    FIGSIZEY = 50
    plt.figure(1, figsize=(FIGSIZEX,FIGSIZEY))
    if LAYOUT == 'neato':
        print "Creating layout..."
        pos = nx.graphviz_layout(G, prog='neato')
    elif LAYOUT == 'geo':
        pos = nodeToGPS
    nodeIDtoUserID = nx.get_node_attributes(G, 'user')
    #colors = [random.random() for r in xrange(nx.number_of_nodes(G))]
    colors = [nodeIDtoUserID[n] for n in G.nodes()]
    # PNG
    #nx.draw_networkx_edges(G,nodeToGPS,edgelist=G.edges(), edge_color='black', width=0.6)
    #nx.draw_networkx_nodes(G,nodeToGPS,node_size=100,node_color=colors,with_labels=False,arrows=True)
    # PDF
    nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.1)
    nx.draw_networkx_nodes(G,pos,node_size=60,node_color=colors,with_labels=False,arrows=True)
    plt.axis('off')
    filename = '%s/graph_%s.pdf' % fileID
    plt.savefig(filename, dpi=250)
    print 'Graph drawn: ' + filename

def getColors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(tuple(colorsys.hls_to_rgb(hue, lightness, saturation)))
    return colors
    
def addExchangeEdges(G):  
    for (_, _, nodeID1, nodeID2, lat1, lon1, dt1, lat2, lon2, dt2) in routing_opportunities: 
        w = abs(toUnix(dt1) - toUnix(dt2))+1 # Phast does not like 0 weights
        G.add_edge(nodeID1, nodeID2, weight=w)
        G.add_edge(nodeID2, nodeID1, weight=w)

def writeMeetingMatrix():
    numUsers = len(userToMonotonicID.keys())
    D = np.empty((numUsers, numUsers))  
    for (_, _, userID1, userID2, lat1, lon1, dt1, lat2, lon2, dt2) in routing_opportunities:
        w = abs(toUnix(dt1) - toUnix(dt2))
        mMax = abs(toUnix(day_start_dt) - toUnix(day_end_dt))
        try:
            m = 1.0/w
        except ZeroDivisionError:
            m = mMax
        D[userID1][userID2] = 1
        D[userID2][userID1] = 1
    D = csr_matrix(D, dtype=float)
    savemat('%s/Meetings_%s.mat' % fileID, {'D' : D}, oned_as='column')
    print 'Meetings written'
    
def toUnix(dt):
    return int(dt.strftime('%s'))

def updateBoundary(tweet):
    global left, right, top, bottom
    top = max(tweet.lat, top)
    bottom = min(tweet.lat, bottom)
    left = min(tweet.lon, left)
    right = max(tweet.lon, right)

def getFlights(G):
    """ 
    Write all edges of G (=user displacements) in a matlab file. Each line is an edge. 
    userID distanceTraveled timeTraveled
    """
    D = np.empty((G.number_of_edges(), 3))    
    for (i, (u, v)) in enumerate(G.edges()):        
        D[i][0] = G.node[u]['user']
        (lat1, lon1) = (G.node[u]['lat'], G.node[u]['lon'])
        (lat2, lon2) = (G.node[v]['lat'], G.node[v]['lon'])
        D[i][1] = calcDistanceOptimized(lat1, lon1, lat2, lon2)
        t1 = toUnix(G.node[u]['dt'])
        t2 = toUnix(G.node[v]['dt'])
        D[i][2] = t2-t1        
    savemat('%s/Flights_%s.mat' % fileID, {'D' : D}, oned_as='column')
    print 'Flights extracted'

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % (round(255*rgb[2]), round(255*rgb[1]), round(255*rgb[0]))
    
def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(rgb_to_hex(colorsys.hls_to_rgb(hue, lightness, saturation)))            
    return colors
    
def get_heatmap_colors(num_colors, heatmap_type):
    colors=[]
    cm = get_cmap(heatmap_type)
    for i in range(num_colors):
        colors.append(rgb_to_hex(cm(1.*i/num_colors)[0:3]))  # color will now be an RGBA tuple
    return colors
    
def getStylesForUsers(userIDs):   
    colors = get_colors(512)
    returnString = ''
    for c in xrange(0,512):        
        returnString += """
<Style id="%d">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff%s</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>""" % (c, colors[c])
    return returnString

def getStylesForHeatmap(num_colors):   
    colors = get_heatmap_colors(num_colors, 'jet') #gist_rainbow # http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
    returnString = ''
    for c in xrange(0, num_colors):
        returnString += """
<Style id="%d">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff%s</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>""" % (c, colors[c])
    returnString += """
<Style id="mismatch">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>fff30fc5</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
"""
    return returnString
    
def getStylesForGreenRedFlights():   
    returnString = """
<Style id="green">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff00ff00</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
<Style id="red">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff0000ff</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
<Style id="yellow">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff00ffff</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
"""
    return returnString

def writeAnimatedKML(content):
    fout_kml = open('%s/animated_%s.kml' % fileID, 'w')
    fout_kml.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">')
    fout_kml.write('<Document><name>Twitter Flights (%s)</name><Folder>\n%s</Folder></Document></kml>' % (fileID[1], content))
    fout_kml.close()
    
def writeAnimatedRedGreenKML(content):
    fout_kml = open('%s/animated_red-green_%s.kml' % fileID, 'w')
    fout_kml.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">')
    fout_kml.write('<Document><name>Twitter Flights Matched with Drive Time (%s)</name><Folder>\n%s</Folder></Document></kml>' % (fileID[1], content))
    fout_kml.close()
    
def write_graph_dimacs(filename, Gint):
    fout = open(filename, 'w')    
    fout.write('p sp %d %d\n' % (nx.number_of_nodes(Gint), Gint.number_of_edges()))
    for (u, v) in Gint.edges():
        fout.write('a %d %d %d\n' % (u, v, Gint[u][v]['weight']))
    fout.close()    

def get_all_pairs_phast(Gint, cells, targetNodes, allOrTweetsOnly):
    print 'Calculating path lengths for all pairs nodes...'
    GintFileName = '%s/Gint_%s.gr' % fileID
    write_graph_dimacs(GintFileName, Gint)
    print 'DIMACS graph written: %s' % GintFileName
    
    # Designate nodes for which we want pairwise shortest paths    
    fout_nodes = open('%s/Gint_%s.nodes' % fileID, 'w')
    if allOrTweetsOnly == 'ALL':
        for cell in cells:
            fout_nodes.write('%d\n' % cell.id)        
        print '%d cells written out as targets' % len(cells)
    elif allOrTweetsOnly == 'TWEETS_ONLY':
        for node in targetNodes:
            fout_nodes.write('%d\n' % node)        
        print '%d nodes written out as targets' % len(targetNodes)
    else:
        print 'Invalid argument: %s' % allOrTweetsOnly
        exit(-1)
    fout_nodes.close()
    
    # Prepare BAT file to run MSR's PHAST
    prefix = '%s\\Gint_%s' % fileID
    fout_bat = open('call_phast_%s.bat' % fileID[1], 'w')
    #if not(fileExists('%s.phast' % prefix)): # only preprocess if the PHAST file is missing
    fout_bat.write('"PartialPHAST2\\x64\\Release\\preprocessing.exe" -M 0 -g %s\n' % prefix)
    fout_bat.write('"PartialPHAST2TestSimple\\App_PartialPHAST2ManyToMany\\bin\\Debug\\App_PartialPHAST2ManyToMany.exe" %s.phast %s.nodes %s.out\n' % (prefix, prefix, prefix))
    fout_bat.write('EXIT\n')
    fout_bat.close()
    #raw_input("Press Enter once all pairs of paths have been computed... (run call_phast.bat)")
    #exit()
    
    # Read shortest paths lengths
    fin_lengths = open('%s/Gint_%s.out' % fileID, 'r')
    lengths = Ddict(dict) # 2D dictionary
    for line in fin_lengths:
        (u, v, length) = line.split()
        lengths[int(u)][int(v)] = int(length)
    fin_lengths.close()    
    return lengths

def printConnectedComponents(G):
    comps = []
    for comp in nx.weakly_connected_component_subgraphs(G):
        comps.append(len(comp.nodes()))
    print sorted(comps)
    print 'Number of connected components: %d' % nx.number_weakly_connected_components(G)

def writeCellKML(cells):
    fout_kml = open('%s/cells_%s.kml' % fileID_short, 'w')
    fout_kml.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">')
    fout_kml.write('<Document><name>Cells</name><Folder>')    
    for cell in cells:
        fout_kml.write('<Placemark><name>%s: %d tweets</name><Polygon><extrude>1</extrude><outerBoundaryIs><LinearRing><coordinates>' % (cell.id, cell.num_tweets))
        fout_kml.write('%f,%f\n' % (cell.left, cell.top))
        fout_kml.write('%f,%f\n' % (cell.right, cell.top))
        fout_kml.write('%f,%f\n' % (cell.right, cell.bottom))
        fout_kml.write('%f,%f\n' % (cell.left, cell.bottom))
        fout_kml.write('%f,%f\n' % (cell.left, cell.top))
        fout_kml.write('</coordinates></LinearRing></outerBoundaryIs></Polygon>\n')
        #fout_kml.write('<Point><coordinates>%f,%f</coordinates></Point>' % (cell.center_lon, cell.center_lat))
        fout_kml.write('<Style><LineStyle><color>990000ff</color><width>2</width></LineStyle><PolyStyle><color>00000000</color></PolyStyle>\n')
        #fout_kml.write('<BalloonStyle><text>Cell ID: %s<BR/>Number of Tweets: %d</text></BalloonStyle>' % (cell.id, cell.num_tweets))
        fout_kml.write('</Style></Placemark>\n')
    fout_kml.write('</Folder></Document></kml>')
    fout_kml.close()

def writeCellPickle(cells): 
        pickle.dump(cells, open('%s/cells_%s.pickle' % fileID_short, 'wb'), -1)
    
def addCellToGraph(G, cell, tweets):
    """ Modify graph: add bi-directional edges between the center of the cell and all tweets within it """
    G.add_node(cell.id)           
    for tweet in tweets:
        w = int(round(calcDistanceOptimized(cell.center_lat, cell.center_lon, tweet.lat, tweet.lon) / 1.4))+1 # time with normal walking speed
        G.add_edge(cell.id, tweet.tweetID, weight=w)
        G.add_edge(tweet.tweetID, cell.id, weight=w)

def findMinRouteLength(tweetsInCell1, tweetsInCell2, lengths):
    """ Consider all pairs of tweets in the two cells and return the cost of the shortest route among all possible routes from cell1 to cell2. """
    minCost12 = float('inf')
    minCost21 = float('inf')
    for t1 in tweetsInCell1:
        for t2 in tweetsInCell2:
            try:
                minCost12 = min(minCost12, lengths[t1.tweetID][t2.tweetID])
            except KeyError:
                pass
            try:
                minCost21 = min(minCost12, lengths[t2.tweetID][t1.tweetID])
            except KeyError:
                pass    
    return (minCost12, minCost21)

def getCells(cellStartID):
    if MIN_DEGREE != None or MAX_SAMPLE_TWEETS != None : # Only write the grid when we are processing the entire dataset (unfiltered node degree and no sampling)
        print 'Loading cells from %s ...' % ('%s/cells_%s.pickle' % fileID_short)
        return pickle.load(open('%s/cells_%s.pickle' % fileID_short, 'rb'))
    print 'Creating cells...'
    global left, right, top, bottom
    print 'Boundary:'
    print 'Left: %f' % left
    print 'Right: %f' % right
    print 'Top: %f' % top
    print 'Bottom: %f' % bottom
    degreesY = CELL_SIZE*0.00000900507679 # this many degrees make up 1 meter at NYC latitude
    degreesX = CELL_SIZE*0.00001183569359
    lons = np.arange(left, right+degreesX, degreesX)
    lats = np.arange(bottom, top+degreesY, degreesY)
    print 'Cell size: %.2f meters' % calcDistanceOptimized(lats[0], lons[0], lats[0], lons[1])
    cells = []
    for x in xrange(0,len(lons)-1):
        for y in xrange(0,len(lats)-1):
            tweetsInCell = [n for n in geoIndex.intersection((lons[x], lats[y], lons[x+1], lats[y+1]), objects=False)]
            if len(tweetsInCell) < 1:
                continue        
            newCell = Cell(cellStartID, lons[x], lats[y], lons[x+1], lats[y+1], 0)
            cellStartID += 1
            cells.append(newCell)
    writeCellKML(cells)  
    writeCellPickle(cells)
    print 'Cells created: %d' % len(cells)
    return cells 
    
def tesselateMap(G, geoIndex, allOrTweetsOnly, cellStartID, userToPath):
    cells = getCells(cellStartID)
    targetNodes = set() # calculate shortest paths only between pairs of these nodes
    cellIDtoSampledTweets = {}
    for cell in cells:
        tweetsInCell = [n.object for n in geoIndex.intersection((cell.left, cell.bottom, cell.right, cell.top), objects=True)]
        cell.num_tweets = len(tweetsInCell)
        np.random.shuffle(tweetsInCell)
        cellIDtoSampledTweets[cell.id] = tweetsInCell[:MAX_SAMPLE_TWEETS]
        targetNodes |= set([tweet.tweetID for tweet in tweetsInCell[:MAX_SAMPLE_TWEETS]])
        if allOrTweetsOnly == 'ALL':                
            addCellToGraph(G, cell, tweetsInCell)
    #T = set([n.object.tweetID for n in geoIndex.intersection((-1000,-1000,1000,1000), objects=True)])    
    #S = set([n.tweetID for n in all_tweets])
    #for t in S.symmetric_difference(targetNodes):
    #    print 'Unaccounted for node: %d' % t
    lengths = get_all_pairs_phast(G, cells, targetNodes, allOrTweetsOnly)
    #lengthsDij = nx.all_pairs_dijkstra_path_length(G)
    #_, lengths = nx.floyd_warshall_predecessor_and_distance(G)
    deliverToPeople(lengths, userToPath)
    writeCoverageMatrixWithoutCellCenters(cells, lengths, cellIDtoSampledTweets)

def deliverToPeople(lengths, userToPath):       
    """
        Motivation: deliver to a given person as fast as possible, but not at any specific location. Simply *wherever* is best.
        Measure the delivery time from the first tweet of person x to any tweet of person y, over all x and y.
    """
    print 'Calculating delivery to PEOPLE...'
    numUsers = len(userToPath.keys())
    D = np.empty((numUsers*(numUsers-1), 6))
    i = 0
    # Find shortest path from the first available tweet of userID1 to any tweet of userID2
    for (userID1, path1) in userToPath.items():
        (nodeID1, dt1, lat1, lon1) = path1[0]
        numTweets1 = len(path1)
        for (userID2, path2) in userToPath.items():
            if userID1 == userID2:
                continue
            numTweets2 = len(path2)
            minTime = float('inf') # fastest delivery time
            minDistance = float('inf') # the closest userID2 ever gets to the first tweet of userID1
            for (nodeID2, dt2, lat2, lon2) in path2:
                try:
                    minTime = min(minTime, lengths[nodeID1][nodeID2])                    
                except KeyError:
                    pass
                minDistance = min(minDistance, calcDistanceOptimized(lat1, lon1, lat2, lon2))
            D[i] = [userID1, userID2, numTweets1, numTweets2, minTime, minDistance]
            i += 1
    savemat('%s/people_delivery_%s.mat' % fileID, {'D' : D}, oned_as='column')
    
def writeCoverageMatrixWithoutCellCenters(cells, lengths, cellIDtoSampledTweets):
    totalTweets = 0
    for c1 in cells:
        totalTweets += len(cellIDtoSampledTweets[c1.id])
    print 'Number of tweets in all cells: %d' % totalTweets
    numPairs = (len(cells)*len(cells)-len(cells))/2
    D = np.empty((numPairs, 7))
    D.fill(float('inf'))
    pairNum = 0
    for (i, c1) in enumerate(cells):
        tweetsInCell1 = cellIDtoSampledTweets[c1.id]
        for (j, c2) in enumerate(cells):
            if j >= i:
                break
            tweetsInCell2 = cellIDtoSampledTweets[c2.id]
            (minLengthOverPairsOfTweets12, minLengthOverPairsOfTweets21) = findMinRouteLength(tweetsInCell1, tweetsInCell2, lengths)
            d = calcDistanceOptimized(c1.center_lat, c1.center_lon, c2.center_lat, c2.center_lon)            
            D[pairNum] = [i, j, c1.num_tweets, c2.num_tweets, minLengthOverPairsOfTweets12, minLengthOverPairsOfTweets21, d]            
            pairNum += 1                                 
        if pairNum%1000 == 0:
            print '%.2f%% cells done.' % (float(pairNum)/numPairs*100)
    savemat('%s/D_%s.mat' % fileID, {'D' : D}, oned_as='column')

def readDriveTimes():
    fileName = '%s/route_times_%s_drive_times.txt' % (baseDir, geoBaseName)        
    drives = Ddict(dict)
    if not(fileExists(fileName)):
        print '! NO DRIVE TIMES FOUND IN FILE %s !' % fileName
        print 'Will approximate with straight line flights.'
        return drives
    fin = open(fileName, 'r')
    maxPossibleDrivingTime = calcDistanceOptimized(bottom, left, top, right) / (40.0/3.6) # max approx. time it would take to drive diagonal distance in the dataset's boudning box
    for line in fin:
        try:
            (ids, lat1, lon1, lat2, lon2, driving_time) = line.split()
        except ValueError:
            print 'Skipping line'
            continue        
        driving_time = int(driving_time)
        dist = calcDistanceOptimized(float(lat1), float(lon1), float(lat2), float(lon2))
        if driving_time > maxPossibleDrivingTime:
            driving_time = dist / (40.0/3.6)
        elif driving_time < 2:
            driving_time = dist / 1.4 # walking speed
        # ids example: 4-1325406539_4-1325411773    
        (id1, id2) = ids.split('_')
        drives[id1][id2] = driving_time # seconds
    return drives
    
def visualizeDriveTimeMatches(userToPath):    
    """ Show people who match the drive time for a given flight in green, others in red """
    THRESHOLD = 900 # seconds
    NUM_HEATMAP_COLORS = 512
    print 'Matching driving times with difference in time between consecutive tweets ...'
    drives = Ddict(dict) #readDriveTimes()
    # Find extremes in deltaT and driveTime
    maxDiff = 0
    minDiff = sys.maxint
    maxDeltaT = 0
    for (userID, path) in userToPath.items():
        for i in xrange(0, len(path)-1):
            (_, dt1, lat1, lon1) = path[i]
            (_, dt2, lat2, lon2) = path[i+1]
            # If driving time matches with some tolerance, show this flight with a green pin
            dist = calcDistanceOptimized(lat1, lon1, lat2, lon2)
            deltaT = dt2-dt1
            if len(drives) > 0:
                driveTime = drives['%d-%d' % (userID,dt1)]['%d-%d' % (userID,dt2)]
            else:
                driveTime = dist/(60.0/3.6)            
            diff = deltaT - driveTime
            maxDeltaT = max(maxDeltaT, deltaT)
            maxDiff = max(maxDiff, diff)
            minDiff = min(minDiff, diff)
    print 'MaxDeltaT: %d MinDiff: %.0f MaxDiff: %.0f' % (maxDeltaT, minDiff, maxDiff)
    # Write animated KML  
    #KMLcontent = getStylesForGreenRedFlights()
    KMLcontent = getStylesForHeatmap(NUM_HEATMAP_COLORS)
    for (userID, path) in userToPath.items():
        for i in xrange(0, len(path)-1):
            (_, dt1, lat1, lon1) = path[i]
            (_, dt2, lat2, lon2) = path[i+1]
            # If driving time matches with some tolerance, show this flight with a green pin
            dist = calcDistanceOptimized(lat1, lon1, lat2, lon2)
            deltaT = dt2-dt1
            driveTime = dist/(60.0/3.6)
            color = int(round( (NUM_HEATMAP_COLORS-1) * ((deltaT - driveTime - minDiff)/(maxDiff-minDiff))))
            if (deltaT - driveTime) < -THRESHOLD: # driving time is longer than deltaT with tolerance!
                color = 'mismatch'
            # if abs(deltaT - driveTime) <= THRESHOLD: # seconds
                # color = 'green'
            # elif (deltaT - driveTime) > 0: # driving time is shorter than deltaT
                # color = 'red'
            # elif (deltaT - driveTime) < 0: # driving time is longer than deltaT!
                # color = 'yellow'
            # else:
                # print 'Unexpected combination'
                # exit(-1)
            #print deltaT, int(round(driveTime)), deltaT - driveTime, color
            dt1_string = datetime.fromtimestamp(dt1).strftime("%m/%d/%Y %I:%M:%S %p")
            dt2_string = datetime.fromtimestamp(dt2).strftime("%m/%d/%Y %I:%M:%S %p")
            KMLcontent += '<Placemark><styleUrl>#%s</styleUrl><name>%s (%d)</name><description>%s %s</description><gx:Track>' % (color, userIDToName[userID], userID, dt1_string, dt2_string)
            KMLcontent += '<when>%s</when>' % datetime.fromtimestamp(dt1).strftime('%Y-%m-%dT%H:%M:%SZ')
            KMLcontent += '<gx:coord>%f %f</gx:coord>' % (lon1, lat1)
            KMLcontent += '<when>%s</when>' % datetime.fromtimestamp(dt2).strftime('%Y-%m-%dT%H:%M:%SZ')
            KMLcontent += '<gx:coord>%f %f</gx:coord>' % (lon2, lat2)
            KMLcontent += '</gx:Track></Placemark>\n'
    writeAnimatedRedGreenKML(KMLcontent)
    
def getTweetTimeDiffDistanceCorrelation(userToPath, numTweets):
    """ Write a matlab file (DT_*.mat) with distance travelled between consecutive tweets and the time diff between them.
    
        Write another matlab file (Tdwell_*.mat) with all dwell times using the userToPath structure
        (toUnix(tweet.dt), tweet.lat, tweet.lon)
        Dwell time is defined as the difference between times of two _consecutive_ tweets of a person, within 100m of each other.
        The actual dwell time can be larger or smaller because tweets are an incomplete sample of actual location.
    """
    print 'Writing distances, travel times, and dwell times for consecutive tweets...'
    DT = np.empty((numTweets, 2))
    idx = 0
    dwells = []
    fout_route = open('%s/route_times_%s.input' % (baseDir, geoBaseName), 'w')
    fout_route.write('ID_From_To\tLatitude From\tLongitude From\tLatitude To\tLongitude To\n')
    for (userID, path) in userToPath.items():
        for i in xrange(0, len(path)-1):
            (_, dt1, lat1, lon1) = path[i]
            (_, dt2, lat2, lon2) = path[i+1]
            fout_route.write('%d-%s_%d-%s\t%.8f\t%.8f\t%.8f\t%.8f\n' %(userID, dt1, userID, dt2, lat1, lon1, lat2, lon2))
            dist = calcDistanceOptimized(lat1, lon1, lat2, lon2)
            deltaT = abs(dt2-dt1)
            if dist < 100:
                dwells.append((userID, deltaT))
            DT[idx] = [deltaT, dist]
            idx += 1
    fout_route.close()
    savemat('%s/DT_%s.mat' % fileID, {'DT' : DT}, oned_as='column')            
    Tdwell = np.empty((len(dwells), 2))
    for (i, (userID, dwellTime)) in enumerate(dwells):
        Tdwell[i] = [userID, dwellTime]
    savemat('%s/Tdwell_%s.mat' % fileID, {'Tdwell' : Tdwell}, oned_as='column')

    # Write animated KML
    print 'Writing animated KML...'
    KMLcontent = getStylesForUsers(userToPath.keys())
    for (userID, path) in userToPath.items():
        KMLcontent += '<Placemark><styleUrl>#%d</styleUrl><name>%d</name><gx:Track>' % (userID%512, userID)
        #KMLcontent += '<Placemark><gx:Track>'
        for stop in sorted(path, key=operator.itemgetter(0)):          
            KMLcontent += '<when>%s</when>' % datetime.fromtimestamp(stop[0]).strftime('%Y-%m-%dT%H:%M:%SZ')
            KMLcontent += '<gx:coord>%f %f</gx:coord>' % (stop[2], stop[1])
        KMLcontent += '</gx:Track></Placemark>\n'
    writeAnimatedKML(KMLcontent)           

def filterUsers(routing_opportunities):
    print 'Inducing meeting graph ...'
    Gm = nx.Graph()
    users = set()
    for (userID1, userID2, tweetID1, tweetID2, lat1, lon1, dt1, lat2, lon2, dt2) in routing_opportunities:
        users.add(userID1)
        users.add(userID2)
        Gm.add_edge(userID1, userID2)    
    print nx.info(Gm)
    components = nx.connected_component_subgraphs(Gm)
    print 'Diameter: %d' % nx.diameter(components[0])
    keepUsers = set([userID for (userID, degree) in Gm.degree().items() if degree >= MIN_DEGREE])
    print 'Max node degree: %d' % max(Gm.degree().values())
    print 'Users left after filtering: %d' % (len(keepUsers))
    return keepUsers
            
def updateUserToPath(userToPath, tweet):
    newStop = (tweet.tweetID, toUnix(tweet.dt), tweet.lat, tweet.lon)
    try:
        userToPath[tweet.userID].append(newStop)
    except KeyError:
        userToPath[tweet.userID] = [newStop]           

def rename_routing_opportunities(routing_opportunities, oldTweetIDtoNew):
    new_routing_opportunities = []
    for (userID1, userID2, tweetID1, tweetID2, lat1, lon1, dt1, lat2, lon2, dt2) in routing_opportunities:
        try:
            new_routing_opportunities.append((userID1, userID2, oldTweetIDtoNew[tweetID1], oldTweetIDtoNew[tweetID2], lat1, lon1, dt1, lat2, lon2, dt2))
        except KeyError: # This routing opportunity became unavailable in the filtered graph
            continue
    return new_routing_opportunities    
        
        

        
        
#LAYOUT = 'neato'    
LAYOUT = 'geo'
COLORS = 'bgrcmyk'
NUM_COLORS = len(COLORS)
MIN_NODES_TO_PLOT = 2  # Plot only users that have at least this many datapoints (nodes)
MAX_NODES_TO_PLOT = sys.maxint #400  # Plot only users that have at most this many datapoints (nodes)
CELL_SIZE = 500 # meters

#ALL_OR_TWEETS_ONLY = 'ALL' # Add cell centers as nodes to the routing graph, connect with bi-dir edges to nearby tweets (old method)
ALL_OR_TWEETS_ONLY = 'TWEETS_ONLY' # Only route on the twitter-flight graph

left = float('inf')
right = -float('inf')
top = -float('inf')
bottom = float('inf')

geoFileName = sys.argv[1]
baseDir = os.path.dirname(geoFileName)
geoBaseName = os.path.splitext(os.path.basename(geoFileName))[0]

G = nx.DiGraph()
userToLastNode = {}
geoIndex = index.Index()
DISTANCE_THRESHOLD = int(sys.argv[2]) #meters
TIME_THRESHOLD = float(sys.argv[3]) # hours
try:
    MAX_SAMPLE_TWEETS = int(sys.argv[4]) # Consider up to MAX_SAMPLE_TWEETS in each cell
except ValueError:
    MAX_SAMPLE_TWEETS = None # Go over all tweets in each cell, when calculating minLengthOverPairsOfTweets
try:
    MIN_DEGREE = int(sys.argv[5]) # Consider only users with node degree at least MIN_DEGREE in the meeting graph; if MIN_DEGREE==None no filtering happens
except ValueError:
    MIN_DEGREE = None # Use all users

print 'DISTANCE_THRESHOLD: %d' % DISTANCE_THRESHOLD
print 'TIME_THRESHOLD: %.2f' % TIME_THRESHOLD
print 'MAX_SAMPLE_TWEETS: %s' % MAX_SAMPLE_TWEETS
print 'MIN_DEGREE: %s' % MIN_DEGREE

fileID = (baseDir, '%s_%dm_%.1fh_%s-sample_%s-degree' % (geoBaseName, DISTANCE_THRESHOLD, TIME_THRESHOLD, MAX_SAMPLE_TWEETS, MIN_DEGREE))
fileID_short = (baseDir, '%s_%dm_%.1fh' % (geoBaseName, DISTANCE_THRESHOLD, TIME_THRESHOLD))
print 'Reading routing_opportunities'
routing_opportunities = pickle.load(open('%s/routing_opportunities_%s.pickle' % fileID_short, 'rb'))
keepUsers = filterUsers(routing_opportunities)
print 'Reading all_tweets'
all_tweets = pickle.load(open('%s/all_tweets_%s.pickle' % (baseDir, geoBaseName), 'rb'))
userToPath = {}
userIDToName = {}

nodeID = 0 # PHAST wants nodes to be numbered from 1, this will be incremented before used for the first time
oldTweetIDtoNew = {} # used to rename tweetIDs/nodeIDs in routing_opportunities
for tweet in all_tweets:
    if MIN_DEGREE != None:
        if not(tweet.userID in keepUsers):
            continue          
    nodeID += 1
    oldTweetIDtoNew[tweet.tweetID] = nodeID
    userIDToName[tweet.userID] = tweet.screen_name
    tweet.tweetID = nodeID
    updateUserToPath(userToPath, tweet)
    geoIndex.insert(long(nodeID), (tweet.lon, tweet.lat, tweet.lon, tweet.lat), obj=tweet)
    try:
        lastNode = userToLastNode[tweet.userID]
    except KeyError:
        userToLastNode[tweet.userID] = MyNode(nodeID, tweet)
        G.add_node(nodeID, user=tweet.userID, lat=tweet.lat, lon=tweet.lon, dt=tweet.dt)
        continue        
    G.add_node(nodeID, user=tweet.userID, lat=tweet.lat, lon=tweet.lon, dt=tweet.dt)
    # Distance edge weights
    #w = calcDistanceOptimized(lastNode.lat, lastNode.lon, tweet.lat, tweet.lon)+1
    # Time edge weights
    w = abs(toUnix(tweet.dt) - toUnix(lastNode.dt))+1 # Phast does not like 0 weights
    G.add_edge(lastNode.nodeID, nodeID, weight=w)
    userToLastNode[tweet.userID] = MyNode(nodeID, tweet)
    updateBoundary(tweet)
    if nodeID % 100000 == 0:
        print '%s lines done' % nodeID

if MIN_DEGREE != None:
    routing_opportunities = rename_routing_opportunities(routing_opportunities, oldTweetIDtoNew)

visualizeDriveTimeMatches(userToPath)    
getTweetTimeDiffDistanceCorrelation(userToPath, len(G.nodes()))
cellStartID = nodeID+1 
print 'Tweets found between the dates: %d' % nodeID
pickle.dump(G, open('%s/G_flights_only_%s.pickle' % fileID, 'wb'), -1)
print nx.info(G)
getFlights(G)
#printConnectedComponents(G)
#writeMeetingMatrix()
addExchangeEdges(G)
pickle.dump(G, open('%s/G_with_exchange_%s.pickle' % fileID, 'wb'), -1)

print nx.info(G)
#printConnectedComponents(G)
tesselateMap(G, geoIndex, ALL_OR_TWEETS_ONLY, cellStartID, userToPath)
#plotGraph(G)