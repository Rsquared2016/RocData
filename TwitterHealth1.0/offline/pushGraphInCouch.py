# Example usage
# python .py ALL.dot_undirected.dot

# See http://networkx.lanl.gov/ for graph routines documentation

import networkx as nx
import sys
import couchdb
import random


""" Instantiate couchdb """
couch = couchdb.Server('http://health.scenedipity.com:5984/')
dbName1 = 'nyc_one_month_friendships'
dbName2 = 'nyc_one_month_friendships_encapsulated'
db1 = couch.create(dbName1) # newly created
db2 = couch.create(dbName2) # newly created

GRAPH_PATH = sys.argv[1]
G = nx.read_dot(GRAPH_PATH)

json = {}
for n1 in sorted(G.nodes()):
    json['$'+n1] = tuple(sorted(G.neighbors(n1))) # escape underscores at the beginning of a key
    (id, rev) = db2.save({'userName': n1, 'friends': sorted(G.neighbors(n1))}) 
    print '%s done' % n1
(id, rev) = db1.save(json)

