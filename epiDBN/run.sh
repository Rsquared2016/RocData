#!/bin/bash

echo
echo "Running feature extraction..."
cd ../features
./run.sh
if [ $? -ne 0 ]; then
	exit 1
fi
cd ../epiDBN

# Number of integer columns in the observations matrix (NUM_INDIVIDUALS + 1 (frame counter))
NUM_OBSERVATIONS=$(cat param_NUM_OBSERVATIONS.txt)
NUM_USERS=$(cat param_NUM_USERS.txt)
NUM_TIME_STEPS=$(cat param_NUM_TIME_STEPS.txt)
OBSERVATION_CARDINALITY=3

echo "NUM_USERS = $NUM_USERS"
echo "NUM_TIME_STEPS = $NUM_TIME_STEPS"
echo "OBSERVATION_CARDINALITY = $OBSERVATION_CARDINALITY"
echo "NUM_OBSERVATIONS = $NUM_OBSERVATIONS"

echo
echo "Decision tree processing..."
rm -f dts/*.dts.index
gmtkDTindex -inputMasterFile dbn.master
if [ $? -ne 0 ]; then
	exit 1
fi

echo
echo "Triangulating..."
rm -rf dbn.str.trifile
gmtkTriangulate -strFile dbn.str -inputMasterFile dbn.master
if [ $? -ne 0 ]; then
	exit 1
fi

./train_cmd.sh $NUM_OBSERVATIONS data/dbn_train_${NUM_TIME_STEPS}.txt
if [ $? -ne 0 ]; then
	exit 1
fi
./test_cmd.sh $NUM_OBSERVATIONS data/dbn_train_${NUM_TIME_STEPS}.txt
if [ $? -ne 0 ]; then
	exit 1
fi