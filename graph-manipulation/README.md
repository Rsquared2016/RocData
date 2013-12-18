This script outputs a graph

```bash
# Requires : brew install graphviz
# Requires : pip intstall networkx matplotlib pygraphviz
# (creating a nice layout takes a long time for large graphs; large means >2000 nodes)
cd ./graph-manipulation
python displaySimpleGraph_demo.py friendship_graph_undirected.dot neato 7
```
