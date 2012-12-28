#!/bin/bash

START="2012-11-17"
END="2012-12-9"

echo
echo "Getting health data from couch..."
python health.py airport_toy health_toy.pickle 0.8 $START $END
if [ $? -ne 0 ]; then
	exit 1
fi

echo
echo "Getting meetings from couch..."
python meetings.py airport_toy meetings_toy.pickle 0.1 1 $START $END
if [ $? -ne 0 ]; then
	exit 1
fi

echo
echo "Checking meetings consistency..."
python check_consistency.py meetings_toy.pickle check_consistency.dump > /dev/null
if [ $? -ne 0 ]; then
	exit 1
fi

echo
echo "Deleting old decision trees..."
rm -f ../epiDBN/dts/*

echo
echo "Creating DBN files..."
python generate_DBN_obs.py health_toy.pickle meetings_toy.pickle
if [ $? -ne 0 ]; then
	exit 1
fi

exit 0