#!/bin/bash

NUM_OBSERVATIONS=$1
TEST=$2
echo $TEST > test.txt

echo
echo "Testing..."

if [ -z "$1" ]
 then
    echo "No testing file specified in arg 1"
    exit
 fi

CMD="gmtkViterbi -strFile dbn.str -triFile dbn.str.trifile -inputMasterFile dbn.master -inputTrainableParameters dbn_trained.params -of1 test.txt -fmt1 ascii -nf1 0 -ni1 $NUM_OBSERVATIONS -verbosity 10 -allocateDenseCpts 2 -vitValsFile dbn_viterbi_states.txt"

echo $CMD
$CMD

#TRUE_LABELS=`basename $TEST .txt`
#DIR_NAME=`dirname $TEST` 
#./verify.sh $DIR_NAME/${TRUE_LABELS}_true_labels.txt