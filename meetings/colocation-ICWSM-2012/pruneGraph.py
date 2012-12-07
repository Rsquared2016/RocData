import networkx as nx
import random
import os.path

########################################################
def bylength(word1, word2):
        """
        returns value > 0 of word1 longer then word2
        returns value = 0 if the same length
        returns value < 0 of word2 longer than word1
        """
        return len(word1) - len(word2)


########################################################
def sampleNodesFromGraph(inputGraph, proportionToKeep): 
        # 0.9 ... keep 90% of the nodes, remove the rest along with incident edges

        filename = inputGraph+'_sampled_'+str(proportionToKeep)
        if os.path.isfile(filename):
                 G = nx.read_dot(filename)
                 print "Cached %s loaded." % filename
                 return G
                 
        Gorig = nx.read_dot(inputGraph)
        G = nx.read_dot(inputGraph)
        #G = nx.Graph(Gorig)
        print "%s loaded." % inputGraph

        nodes = Gorig.nodes()
        random.shuffle(nodes)
        N = len(nodes)
        # keep k nodes
        k = int(round(N*(1-proportionToKeep)))
        
        for n in range(0,k):
                G.remove_node(nodes[n])

        nx.write_dot(G, filename)
        print "\tGraph sampled. Original graph had %d nodes, sampled graph has %d nodes." % (len(Gorig.nodes()), len(G.nodes())) 

        return G

def getNodeColors(G):
        node_color= []
        for n in G.nodes():
                node_color.append( float(len(G.neighbors(n))+ 0.5) )
        return node_color
                        
def convertToUndirectedKeepOnlyReciprocatedEdges(G):
        # find all bi-directional edges
        mutual = []
        for (u,v) in G.edges():
                if G.has_edge(v,u):
                        mutual.append((u,v))
        Gbi = nx.Graph(mutual)
        return Gbi

        ########################################################

def RemoveSmallCliques(inputGraph, MIN_CLIQUE_SIZE=1):
        # remove all cliques of size less than 

        Gorig = inputGraph
        #print "%s loaded." % inputGraph

        ########################################################
        # find all bi-directional edges

        mutual = []

        for (u,v) in Gorig.edges():
                if Gorig.has_edge(v,u):
                        mutual.append((u,v))

        G = nx.Graph(mutual)

        ########################################################
        # find cliques

        cliques = list(nx.find_cliques(G))

        num_cliques = 0
        keep = set()
        NODEtoCOLOR = {}

        print "---------------------------"
        print "Cliques:"
        print "["
        for c in sorted(cliques, cmp=bylength, reverse=True):
                if len(c) < MIN_CLIQUE_SIZE:
                        break
                num_cliques += 1
                print "%s," % (c)
                for node in c:
                        keep.add(node)
                        # colorize nodes
                        color = num_cliques/len(c)
                        try:
                                # blend
                                NODEtoCOLOR[node] = (NODEtoCOLOR[node]+float(color))/2.0
                        except KeyError:
                                NODEtoCOLOR[node] = float(color)

        print "]"
        print "\tCliques considered: %s." % (num_cliques)
        print "---------------------------"

        # remove nodes not belonging to larger cliques
        node_size = []
        node_color = []
        #G = nx.read_dot(inputGraph)
        for n in G.nodes():
                if not(n in keep):
                        G.remove_node(n)
                else:
                        # get node size
                        node_size.append( float(len(Gorig.neighbors(n))) + 0.5)
                        node_color.append( NODEtoCOLOR[n] )

        print "\tNodes kept: %s (out of %s original)." % (len(keep), len(Gorig.nodes()))
        return (G, node_size, node_color)

########################################################

def pruneGraph(inputGraph, MIN_CLIQUE_SIZE=1):
        # remove all cliques of size less than 

        Gorig = nx.read_dot(inputGraph)
        print "%s loaded." % inputGraph

        ########################################################
        # find all bi-directional edges

        mutual = []

        for (u,v) in Gorig.edges():
                if Gorig.has_edge(v,u):
                        mutual.append((u,v))

        G = nx.Graph(mutual)

        ########################################################
        # find cliques

        cliques = list(nx.find_cliques(G))

        num_cliques = 0
        keep = set()
        NODEtoCOLOR = {}

        print "---------------------------"
        print "Cliques:"
        print "["
        for c in sorted(cliques, cmp=bylength, reverse=True):
                if len(c) < MIN_CLIQUE_SIZE:
                        break
                num_cliques += 1
                print "%s," % (c)
                for node in c:
                        keep.add(node)
                        # colorize nodes
                        color = num_cliques/len(c)
                        try:
                                # blend
                                NODEtoCOLOR[node] = (NODEtoCOLOR[node]+float(color))/2.0
                        except KeyError:
                                NODEtoCOLOR[node] = float(color)

        print "]"
        print "\tCliques considered: %s." % (num_cliques)
        print "---------------------------"

        # remove nodes not belonging to larger cliques
        node_size = []
        node_color = []
        #G = nx.read_dot(inputGraph)
        for n in G.nodes():
                if not(n in keep):
                        G.remove_node(n)
                else:
                        # get node size
                        node_size.append( float(len(Gorig.predecessors(n)) + len(Gorig.successors(n)) + 0.5) )
                        node_color.append( NODEtoCOLOR[n] )

        print "\tNodes kept: %s (out of %s original)." % (len(keep), len(Gorig.nodes()))
        return (G, node_size, node_color)


