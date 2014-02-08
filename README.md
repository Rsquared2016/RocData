RocData
=======

Prof. Henry Kautz at University of Rochester's Research Group Repository

## Notes
- There are two database files missing from this repository because of github's
policy changes. I will add links to them ASAP.

- Each folder in this repository should be a standalone application for now.
In the future, each project should be self contained in its own repo, and submoduled here.

- Each repository should have it's own README with instructions.

- The goal for each project is to have 3 commands to build a working environment.

```bash
configure      # should look through any system and find all dependencies for each machine
make           # should generate appropriate makefile
make install   # should compile and install all components necessary
make run       # should start all the services necessary for the given software.
```

## TODO : Organize. 

Get data:
```bash 
cd ./process-tweets
wget http://cs.rochester.edu/~sadilek/log-geo-area_NYC_GPS_sorted_filtered_6237.dat
```

Process data:
```bash 
python -OO processTweets.py 2000 words.txt log-geo-area_NYC_GPS_sorted_filtered_6237.dat
```

Display social graph:
```bash 
cd ./graph-manipulation
```

Render heatmap of twitter flights:
```bash
cd ./heatmap-flights
python heatmap.py -p twitter_1M.coors.txt -r 5 -o NYC_z14_1M_blue.png -G gradient-adam-blue.png --osm -e 40.8393,-74.2635,40.5,-73.6558 -z 14
```


Compile gmtk-2012-12-07_2148 on MAC mountain lion x64
```bash
# on MacOSX
./configure CFLAGS=-m64 CXXFLAGS=-m64 LDFLAGS=-m64 && make && make install

# on linux, just
./configure prefix=.../bin && make && make install
```

to compile with DBN structure visualization (gmtkViz), run this first (throws compile errors though):
```bash
# you'll need to have brew installed first (http://brew.sh/)
brew install wxmac --devel
which wx-config  # To check the version.
```

