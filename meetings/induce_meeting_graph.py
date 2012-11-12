"""
Extract undirected meeting graph: nodes are people, links mean they likely met (appear in routing opportunities)

Example: python -OO induce_meeting_graph.py data/rectangle_DateTime_greater_Seattle_2012_January_10K_uniq.txt

"""

import cPickle as pickle
import colorsys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import sys

from datetime import datetime
from scipy.io import savemat
from utils import *

def getConnectedComponents(G):
    comps = nx.connected_component_subgraphs(G)    
    for comp in comps:
        print len(comp.nodes()),
    print 'Number of connected components: %d' % len(comps)
    return comps

def getColors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(tuple(colorsys.hls_to_rgb(hue, lightness, saturation)))
    return colors
    
def plotGraph(G):
    FIGSIZEX = 50
    FIGSIZEY = 50
    plt.figure(1, figsize=(FIGSIZEX,FIGSIZEY))
    if LAYOUT == 'neato':
        print "Creating layout..."
        pos = nx.graphviz_layout(G, prog='neato')
    elif LAYOUT == 'geo':
        pos = nodeToGPS        
    #colors = [random.random() for r in xrange(nx.number_of_nodes(G))]
    #colors = [nodeIDtoUserID[n] for n in G.nodes()]
    colors = getColors(len(G.nodes()))
    # PNG
    #nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.3, alpha=1)
    #nx.draw_networkx_nodes(G,pos,node_size=60,node_color=colors,with_labels=False,arrows=False, alpha=1, linewidths=0)
    #filename = '%s/graph_%s_%dm_%.1fh.png' % fileNameComponents_short    
    # SVG
    nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.3, alpha=0.8)
    nx.draw_networkx_nodes(G,pos,node_size=40,node_color=colors,with_labels=False,arrows=False, alpha=1, linewidths=0)    
    filename = '%s/graph_%s_%dm_%.1fh.svg' % fileNameComponents_short
    plt.axis('off')    
    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
    print 'Graph drawn: ' + filename

def filterUsers(degreeDict):
    minDegree = 3
    all_tweets = pickle.load(open('%s/all_tweets_%s.pickle' % (baseDir, geoBaseName), 'rb'))
    new_all_tweets = []
    numUsersLeft = sum([1 for degree in degreeDict.values() if degree >= minDegree])
    for tweet in all_tweets:
        try:
            userDegree = degreeDict[tweet.userID]
        except KeyError:
            continue
        if userDegree >= minDegree:
            new_all_tweets.append(tweet)
    pickle.dump(new_all_tweets, open('%s/all_tweets_%s_filtered-users_%d.pickle' % (baseDir, geoBaseName, numUsersLeft), 'wb'), -1)
    
    
    
geoFileName = sys.argv[1]
DISTANCE_THRESHOLD = int(sys.argv[2]) # meters
TIME_THRESHOLD = float(sys.argv[3]) # hours
LAYOUT = 'neato'

baseDir = os.path.dirname(geoFileName)
geoBaseName = os.path.splitext(os.path.basename(geoFileName))[0]

fileNameComponents_short = (baseDir, geoBaseName, DISTANCE_THRESHOLD, TIME_THRESHOLD)
print 'Reading routing_opportunities ...'
routing_opportunities = pickle.load(open('%s/routing_opportunities_%s_%dm_%.1fh.pickle' % fileNameComponents_short, 'rb'))

print 'Inducing graph ...'
G = nx.Graph()
users = set()
for (userID1, userID2, tweetID1, tweetID2, lat1, lon1, dt1, lat2, lon2, dt2) in routing_opportunities:
    users.add(userID1)
    users.add(userID2)
    G.add_edge(userID1, userID2)

print 'Unique users: %d' % len(users)
print nx.info(G)

# Diameter of the largest component
components = getConnectedComponents(G)
print 'Diameter: %d' % nx.diameter(components[0])

# Write node degree distribution
degrees = G.degree().values()
D = np.empty((len(degrees), 1))
D = degrees
savemat('%s/degree_%s_%dm_%.1fh.mat' % fileNameComponents_short, {'Degrees' : D}, oned_as='column')
pickle.dump(G.degree(), open('%s/degree_%s_%dm_%.1fh.pickle' % fileNameComponents_short, 'wb'), -1)

#filterUsers(G.degree())

#plotGraph(components[0])


    