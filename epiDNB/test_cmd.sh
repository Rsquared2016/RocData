#!/bin/bash

#test data points: 3000,9000,15000

if [ -z "$1" ]
 then
    echo "No testing file specified in arg 1"
    exit
 fi

TEST=$1
echo $TEST > test.txt

gmtkViterbi -strFile hmm.str -triFile hmm.str.trifile -inputMasterFile hmm.mtr -inputTrainableParameters trained.params -of1 test.txt -fmt1 ascii -nf1 0 -ni1 3 -verbosity 10 -vitValsFile hmm_vitVals.txt &&

TRUE_LABELS=`basename $TEST .txt`
DIR_NAME=`dirname $TEST` 
./verify.sh $DIR_NAME/${TRUE_LABELS}_true_labels.txt






# if [ -z "$1" ]
# then
#     echo "No num supplied, defaulting to testing data with 15000 samples"
#     TEST="data/hmm_test_15000data.txt"
#     NUM="15000"
# else
#     NUM="$1"
#     TEST="data/hmm_test_${NUM}data.txt"
#     if [ ! -e "$TEST" ]
#     then
#     echo "Num not 3000,9000,15000, defaulting to testing data with 15000 samples"
#     TEST="data/hmm_test_15000data.txt"
#     NUM="15000"
#     fi
# fi
