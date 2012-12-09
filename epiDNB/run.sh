#!/bin/bash

python generate_obs.py

if [ $? -eq 1 ]; then
	exit 1
fi

echo
echo "Triangulating..."
rm -rf dbn.str.trifile
gmtkTriangulate -strFile dbn.str -inputMasterFile dbn.master &&

echo
echo "Decision tree processing..."
rm -f dts/*.dts.index
gmtkDTindex -inputMasterFile dbn.master && true

./train_cmd.sh data/dbn_train_100.txt &&
./test_cmd.sh data/dbn_train_100.txt 