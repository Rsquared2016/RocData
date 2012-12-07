import networkx as nx
import matplotlib.pyplot as plt
import sys
import random
import pruneGraph

class customGraph:

    def __init__(self, filename):
        self.G = None
        self.colors = []
        self.nameSet = set()
        self.filename = ''
        self.N = 0
        self.layout = None
        self.layoutType = ''
        
        self.G = nx.read_dot(filename)
        self.nameSet = set(self.G.nodes())
        self.filename = filename
        print "Graph loaded:"
        print nx.info(self.G)


    def getNodeNameSet(self):
        return self.nameSet

    
    def areFriends(self, A, B):
        return self.G.has_edge(A,B)

    def getFriends(self, A):
        return set(self.G.neighbors(A))

    
    def removeSmallCliques(self, N):
        self.N = N
        (self.G, node_size, node_color) = pruneGraph.RemoveSmallCliques(self.G, N)
        print "Visualizing graph:"
        print nx.info(self.G)


    def convertToUndirectedKeepOnlyReciprocatedEdges(self):
        self.G = pruneGraph.convertToUndirectedKeepOnlyReciprocatedEdges(self.G)
        print "Converted Graph:"
        print nx.info(self.G)
        nx.drawing.nx_agraph.write_dot(self.G, filename+'_undirected.dot')
        #print "Graph saved: "+ GRAPH_PATH+'_undirected.dot'


    def highlightNodes(self, highlight):
        # Colorize sick (red) vs. healthy (blue) individuals
        self.colors= []
        for n in self.G.nodes():
            if n in highlight:
                self.colors.append('#faf102')
            else:
                self.colors.append('#0749f2')

                
    def saveGraph(self):
        nx.write_gml(self.G, '%s.gml' % self.filename)
        nx.drawing.nx_agraph.write_dot(self.G, self.filename+'_gte_'+str(self.N)+'.dot')       

        
    def renderGraph(self, layoutType, suffix):
        """
        layoutType can be: neato, circo, fdp, frl 
        colors can be floats, 'r', 'g', 'b',... , and '#ffffff'
        """

        FIGSIZE = 30
        #FIGSIZE = 10

        # find a nice layout
        plt.figure(1, figsize=(FIGSIZE,FIGSIZE))
        if self.layoutType != layoutType:
            if layoutType == "frl":
                # nice clustering
                # runs out of memory for ALL graph
                pos=nx.fruchterman_reingold_layout(self.G)
            else:
                pos=nx.graphviz_layout(self.G,prog=layoutType) #, hold=True)#, "-Goverlap=scale")
            self.layout = pos
            self.layoutType = layoutType
            print "\tLayout done."

        nx.draw_networkx_edges(self.G, self.layout, edgelist=self.G.edges(), edge_color='black', width=0.1)
        nx.draw_networkx_nodes(self.G, self.layout, node_size=100,node_color=self.colors,with_labels=False)

        #for small graphs
        #nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.5)
        #nx.draw_networkx_nodes(G,pos,node_size=200,node_color=pruneGraph.getNodeColors(G),with_labels=False)
        
        #nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.6)
        #nx.draw_networkx_nodes(G,pos,node_size=20,node_color=pruneGraph.getNodeColors(G),with_labels=False)
        
        # for small PNG graphs
        #nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.8)
        #nx.draw_networkx_nodes(G,pos,node_size=200,node_color=node_color,with_labels=False)
        
        # for small PDF graphs
        #nx.draw_networkx_edges(G,pos,edgelist=G.edges(), edge_color='black', width=0.1)
        #nx.draw_networkx_nodes(G,pos,node_size=500,node_color=node_color,with_labels=False)
        
        ## ########################################################
        
        ## nx.draw(     G,
        ##              pos,
        ##              node_size=2,
        ##              node_color=pruneGraph.getNodeColors(G),
        ##              #edge_color=edge_color,
        ##              with_labels=False,
        ##              #with_labels=True,
        ##              width=0.2,
        ##              #style='dashed',
        ##              #dir='both'
        ##              )

        ########################################################
        # PLOT
        plt.axis('off')
        #outFilename = "%s_%s_gte_%d_%04d.png" % (self.filename, self.layoutType, self.N, suffix)
        outFilename = "%04d.png" % suffix
        plt.savefig(outFilename, dpi=72)
        plt.clf()
        print "\tGraph drawn: "+outFilename
