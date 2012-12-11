#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Set NUM_OBSERVATIONS" >&2
  exit 1
fi

# Number of integer columns in the observations matrix (NUM_INDIVIDUALS + 1 (frame counter))
NUM_OBSERVATIONS=$1
NUM_USERS=$2
NUM_TIME_STEPS=$3
OBSERVATION_CARDINALITY=$4

echo "NUM_USERS = $NUM_USERS"
echo "NUM_TIME_STEPS = $NUM_TIME_STEPS"
echo "OBSERVATION_CARDINALITY = $OBSERVATION_CARDINALITY"

python generate_obs.py $NUM_USERS $NUM_TIME_STEPS $OBSERVATION_CARDINALITY

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

./train_cmd.sh $NUM_OBSERVATIONS data/dbn_train_${NUM_TIME_STEPS}.txt
if [ $? -eq 1 ]; then
	exit 1
fi
./test_cmd.sh $NUM_OBSERVATIONS data/dbn_train_${NUM_TIME_STEPS}.txt 
if [ $? -eq 1 ]; then
	exit 1
fi