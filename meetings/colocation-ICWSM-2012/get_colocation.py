# example:

# to process the first 1000 users:
# python -OO get_colocation.py tweets_WORDS_augmented-50-50-nyc.txt.txt users-nyc.txt 0 999 0.001

# python -OO get_colocation.py tweets_test.txt tweet_test_users.txt 0 2 0.001 24
#
# related to crandall.py
#
# output a file
# userName1 timeSegmentNum userName2 num_colocs@1h num_colocs_unique@1h
#     num_colocs@4h num_colocs_unique@4h
#     num_colocs@12h num_colocs_unique@12h
#     num_colocs@24h num_colocs_unique@24h

# ! NOT ANYMORE, USES TOO MUCH MEMORY
# It also outputs a mapping {}:
# (userName, time_segment) -> {colocated user names -> amount_of_colocation}


import sys
#import networkx as nx
from numpy import *
from readGPStweets import *
from utils import *


def truncatePathToSegment(oldPath, segmentNum):
        newPath = []
        for (unix_time, cell_id) in oldPath:
                #print  unix_time, datetime.fromtimestamp(unix_time)
                if unix_time < START:
                        continue
                if unix_time >= daySegmentsPairs[segmentNum][0] and unix_time <= daySegmentsPairs[segmentNum][1]:
                        newPath.append((unix_time, cell_id))
        return newPath


# NYC bounding box
topLeftLat = 40.808352
topLeftLon = -74.178314
bottomRightLat = 40.57146
bottomRightLon = -73.62728

# ??bounding box for clique-8
topLeftLat = 41.235791
topLeftLon = -74.749047
bottomRightLat = 39.939552
bottomRightLon = -73.029238

print 'North-South length: %.2f meters' % calcDistance(topLeftLat,
                                                       topLeftLon,
                                                       bottomRightLat,
                                                       topLeftLon)

print 'West-East length: %.2f meters' % calcDistance(topLeftLat,
                                                     topLeftLon,
                                                     topLeftLat,
                                                     bottomRightLon)

USER_START = int(sys.argv[3])
USER_END = int(sys.argv[4])

# degrees of dicretization = size of cell side
cell_size = float(sys.argv[5])
#cell_size = 0.01
#cell_size = 0.001

# the time window (in hours) within which we count co-locations
#time_threshold = float(sys.argv[4])

print 'North-South cell size: %.2f meters' % calcDistance(topLeftLat,
                                                          topLeftLon,
                                                          topLeftLat+cell_size,
                                                          topLeftLon)

print 'West-East cell size: %.2f meters' % calcDistance(topLeftLat,
                                                        topLeftLon,
                                                        topLeftLat,
                                                        topLeftLon+cell_size)

num_horiz_cells = 1
num_vert_cells = 1
for lat in arange(bottomRightLat, topLeftLat, cell_size):
    num_vert_cells += 1
for lon in arange(topLeftLon, bottomRightLon, cell_size):
    num_horiz_cells += 1
num_cells = num_horiz_cells * num_vert_cells

print 'Number of cells: %d (horiz=%d, vert=%d)' % (num_cells, num_horiz_cells, num_vert_cells)
#cells = [[0]*num_horiz_cells for x in xrange(num_vert_cells)]


# read GPS-tagged tweets, place each tweet into appropriate cell,
# increment the cell counter
r = readGPStweets(sys.argv[1])
tweet = r.getNextGPS()
num_ignored = 0
num_counted = 0
minLat = 99999999
minLon = 99999999
maxLat = -99999999
maxLon = -99999999

# Create time segments
# For NYC dataset
INTERVAL = 24*3600 # Model with this granularity (seconds)
#START = 1274241600 # Wed May 19 2010 00:00:00 GMT-4
#END = 1277078400 # Sun Jun 20 2010 00:00:00 GMT-4
START = 1274227200 # Wed, 19 May 2010 00:00:00 GMT
END = 1276992000 # Sun, 20 Jun 2010 00:00:00 GMT

daySegments = range(START, END+1, INTERVAL)
daySegmentsPairs = []
for i in range(0,len(daySegments)-1):
      daySegmentsPairs.append((daySegments[i], daySegments[i+1]-1))
      print 'Segment %d: %s -> %s' % (i, datetime.fromtimestamp(daySegmentsPairs[-1][0]), datetime.fromtimestamp(daySegmentsPairs[-1][1]))
      
# read friendship graph
#G = nx.read_dot(sys.argv[2])

# create a "hash set" of usernames
fusers = open(sys.argv[2], 'r')
USERNAMES = {}
for user in fusers:
    USERNAMES[user.strip()] = True
fusers.close()
# 'user1' -> [ (human_time, cell_id), ... ]
USERtoPATH = {}

while tweet != None:
    ((lat, lon), userName, createdAt) = tweet
    
    #print tweet
    tweet = r.getNextGPS()

    # if user is not in the graph, skip it
    try:
        exists = USERNAMES[userName]
    except KeyError:
        num_ignored += 1
        continue

    # get a bounding box that contains ALL tweets
    minLat = min(minLat, lat)
    minLon = min(minLon, lon)
    maxLat = max(maxLat, lat)
    maxLon = max(maxLon, lon)
    
    # if this coordinate is outside of the bounding box, skip it
    if lat < bottomRightLat or lat > topLeftLat or lon < topLeftLon or lon > bottomRightLon:
        num_ignored += 1
        continue
    num_counted += 1 
    
    # get cell coordinates from the continuous GPS coordinates
    cell_x = int(round((lon - topLeftLon)/cell_size))
    cell_y = int(round((lat - bottomRightLat)/cell_size))
    #cells[cell_y][cell_x] += 1

    (human_time, unix_time) = getTime(createdAt)
    cell_id = cell_y*num_horiz_cells + cell_x
    try:
        USERtoPATH[userName].append( (unix_time, cell_id) )
    except KeyError:
        USERtoPATH[userName] = [ (unix_time, cell_id) ]

#print USERtoPATH
#for row in cells:
#    print row

print '# GPS readings outside bounding box: %d' % num_ignored
print '# GPS readings inside bounding box: %d' % num_counted

print 'topLeftLat = %f' % maxLat
print 'topLeftLon = %f' % minLon
print 'bottomRightLat = %f' % minLat
print 'bottomRightLon = %f' % maxLon

# calculate conditional probabilities: Pr(A B are friends | colocation_amount=x)
users = USERtoPATH.keys()
print users
CPD = {}
#(userName, time_segment) -> {colocated user names -> amount_of_colocation}
userAndSegmentToColocation = {}
f_colocs = open('%s_colocs_%d-%d' % (sys.argv[1], USER_START, USER_END), 'w')
for i,A in enumerate(users):
        if i<USER_START or i>USER_END:
                continue
        for B in users[:i]:
                # limit path to be only within a time segment
                for segmentNum in range(0,len(daySegmentsPairs)):
                        newPathA = truncatePathToSegment(USERtoPATH[A], segmentNum)
                        newPathB = truncatePathToSegment(USERtoPATH[B], segmentNum)
                        num_colocs_unique = []
                        num_colocs = []                
                        for time_threshold in [1, 4, 12, 24]:
                                #print newPathA         
                                #print newPathB
                                if len(newPathA)==0 or len(newPathB)==0:
                                        common_cells = []
                                else:
                                        common_cells = calculateCoLocationsDiscrete(newPathA, newPathB, time_threshold)
                                # count unique cells only
                                num_colocs_unique.append(len(set(common_cells)))
                                # count all cells, including duplicities
                                num_colocs.append(len(common_cells))

                        if sum(num_colocs) > 0 or sum(num_colocs_unique) > 0:
                                f_colocs.write('%s %d %s ' % (A, segmentNum, B))                        
                                for (n, nu) in zip(num_colocs, num_colocs_unique):
                                        f_colocs.write('%d %d ' % (n, nu))
                                f_colocs.write('\n')
                                #try:
                                #    dic = userAndSegmentToColocation[(A,segmentNum)]
                                #except KeyError:
                                #    dic = {}
                                #dic[B] = num_colocs    
                                #userAndSegmentToColocation[(A,segmentNum)] = dic

                                #try:
                                #    dic = userAndSegmentToColocation[(B,segmentNum)]
                                #except KeyError:
                                #    dic = {}
                                #dic[A] = num_colocs    
                                #userAndSegmentToColocation[(B,segmentNum)] = dic


        print 'User %s (%d) done.' % (A, i)
f_colocs.close()
#import pickle
#pickle.dump( userAndSegmentToColocation, open( "userAndSegmentToColocation.pickle", "wb" ) )

#for (userAndSegment, coloc_dic) in sorted(userAndSegmentToColocation.items()):
#        (user, segmentNum) = userAndSegment
#        print '%s [%d] (%s -> %s): ' % (user, segmentNum, datetime.fromtimestamp(daySegmentsPairs[segmentNum][0]), datetime.fromtimestamp(daySegmentsPairs[segmentNum][1]))
#        for (otherUser, coloc) in coloc_dic.items():
#                print '\t%s: %d' % (otherUser, coloc)

                
