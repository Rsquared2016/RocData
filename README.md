Get data:
cd process-tweets
wget http://cs.rochester.edu/~sadilek/log-geo-area_NYC_GPS_sorted_filtered_6237.dat

Process data:
python -OO processTweets.py 2000 words.txt log-geo-area_NYC_GPS_sorted_filtered_6237.dat

Display social graph:
cd graph-manipulation
python displaySimpleGraph_demo.py friendship_graph_undirected.dot neato 7
(creating a nice layout takes a long time for large graphs; large means >2000 nodes)

Render heatmap of twitter flights:
cd heatmap-flights
python heatmap.py -p twitter_1M.coors.txt -r 5 -o NYC_z14_1M_blue.png -G gradient-adam-blue.png --osm -e 40.8393,-74.2635,40.5,-73.6558 -z 14
