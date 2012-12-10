#!/bin/bash

python generate_obs.py

if [ $? -eq 1 ]; then
	exit 1
fi

echo
echo "Triangulating..."
rm -rf dbn.str.trifile
gmtkTriangulate -strFile dbn.str -inputMasterFile dbn.master

if [ $? -eq 1 ]; then
	exit 1
fi

echo
echo "Decision tree processing..."
rm -f dts/*.dts.index
gmtkDTindex -inputMasterFile dbn.master

if [ $? -eq 1 ]; then
	exit 1
fi

./train_cmd.sh data/dbn_train_100.txt
if [ $? -eq 1 ]; then
	exit 1
fi
./test_cmd.sh data/dbn_train_100.txt 
if [ $? -eq 1 ]; then
	exit 1
fi