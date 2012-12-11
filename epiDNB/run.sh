#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Set NUM_OBSERVATIONS" >&2
  exit 1
fi

# Number of integer columns in the observations matrix (NUM_INDIVIDUALS + 1 (frame counter))
NUM_OBSERVATIONS=$1

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

./train_cmd.sh $NUM_OBSERVATIONS data/dbn_train_100.txt
if [ $? -eq 1 ]; then
	exit 1
fi
./test_cmd.sh $NUM_OBSERVATIONS data/dbn_train_100.txt 
if [ $? -eq 1 ]; then
	exit 1
fi