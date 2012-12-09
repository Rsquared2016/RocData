#!/bin/bash

python generate_obs.py &&

echo
echo "Triangulating..."
rm -rf dbn.str.trifile
gmtkTriangulate -str dbn.str -inputM dbn.mtr &&

echo
echo "Decision tree processing..."
rm -f dts/*.dts.index
DT_FILES=$(ls dts/*.dts)
for f in $DT_FILES
do
	gmtkDTindex -decisionTreeFiles $f && true
done

./train_cmd.sh data/dbn_train_100.txt &&
./test_cmd.sh data/dbn_train_100.txt 