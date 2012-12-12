#!/bin/bash

# Number of integer columns in the observations matrix (NUM_INDIVIDUALS + 1 (frame counter))
NUM_OBSERVATIONS=$(cat param_NUM_OBSERVATIONS.txt)
NUM_USERS=$(cat param_NUM_USERS.txt)
NUM_TIME_STEPS=$(cat param_NUM_TIME_STEPS.txt)
OBSERVATION_CARDINALITY=3

echo "NUM_USERS = $NUM_USERS"
echo "NUM_TIME_STEPS = $NUM_TIME_STEPS"
echo "OBSERVATION_CARDINALITY = $OBSERVATION_CARDINALITY"

echo
echo "Deleting old decision trees..."
rm -f dts/*

echo
echo "Running feature extraction..."
# ./run.sh 4 3 6 3
#python generate_obs_toy.py $NUM_USERS $NUM_TIME_STEPS $OBSERVATION_CARDINALITY

cd ../features
./run.sh
cd ../epiDBN

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