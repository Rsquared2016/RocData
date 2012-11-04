# Example usage
# python displaySimpleGraph_demo.py friendhip_graph_undirected.dot neato 7

# You need to install matplotlib library and python hooks to it and networkx
# For python hooks, use easy_install command with --install-dir option (if you don't have root access)
# See http://networkx.lanl.gov/ for graph routines documentation

import networkx as nx
import matplotlib.pyplot as plt
import sys
import random
import pruneGraph


########################################################
########################################################
## MAIN

FIGSIZEX = 30
FIGSIZEY = 30
#FIGSIZE = 10


GRAPH_PATH = sys.argv[1]

# neato, circo, fdp, frl
PROG = sys.argv[2]

# Display only cliques larger or equal to N
N = int(sys.argv[3])


G = nx.read_dot(GRAPH_PATH)

print "Original Graph:"
print nx.info(G)

# display only the large conected component
#C = nx.algorithms.components.connected.connected_components(G)
#for c in C:
#    if len(c) > 5000:
#        G = G.subgraph(c)

# Display only cliques larger or equal to N
#(G, node_size, node_color) = pruneGraph.RemoveSmallCliques(G, N)
#nx.drawing.nx_agraph.write_dot(G, GRAPH_PATH+'_gte_'+str(N)+'.dot')
#print "Pruned Graph:"
#print nx.info(G)

########################################################
# find a nice layout

plt.figure(1, figsize=(FIGSIZEX,FIGSIZEY))

if PROG == "frl":
    # nice clustering
    # runs out of memory for ALL graph
    pos=nx.fruchterman_reingold_layout(G)
else:
    pos=nx.graphviz_layout(G,prog=PROG) #, hold=True)#, "-Goverlap=scale")

print "\tLayout done."

nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.6)
nx.draw_networkx_nodes(G,pos,node_size=120,node_color=node_color,with_labels=False)

# PLOT
plt.axis('off')
filename = "%s_%s_gte_%d.png" % (GRAPH_PATH, PROG, N)
plt.savefig(filename, dpi=150)
print "\tGraph drawn: "+filename

