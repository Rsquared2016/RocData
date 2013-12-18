## Setup.
```bash
# Requires : brew install graphviz
# Requires : pip intstall networkx matplotlib pygraphviz
# (creating a nice layout takes a long time for large graphs; large means >2000 nodes)
cd ./graph-manipulation
python displaySimpleGraph_demo.py friendship_graph_undirected.dot neato 7
```
## Input.
This script takes a data file like so : 

```python
strict graph {
  user -- person_they_follow_1;
  user -- person_they_follow_2;
  ...
  user -- person_they_follow_n;
}
```

## Output.
This script outputs a graph like so : 

![Sample Output](https://raw.github.com/HenryKautz/RocData/master/graph-manipulation/screenie.png?token=747630__eyJzY29wZSI6IlJhd0Jsb2I6SGVucnlLYXV0ei9Sb2NEYXRhL21hc3Rlci9ncmFwaC1tYW5pcHVsYXRpb24vc2NyZWVuaWUucG5nIiwiZXhwaXJlcyI6MTM4Nzk4Nzk5NX0%3D--57cb1cca151d89d41cbee5ab1ddac075d4f55ebf)
