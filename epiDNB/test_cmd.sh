#!/bin/bash

if [ -z "$1" ]
 then
    echo "No testing file specified in arg 1"
    exit
 fi

TEST=$1
echo $TEST > test.txt

gmtkViterbi -strFile dbn.str -triFile dbn.str.trifile -inputMasterFile dbn.mtr -inputTrainableParameters dbn_trained.params -of1 test.txt -fmt1 ascii -nf1 0 -ni1 3 -verbosity 10 -vitValsFile dbn_viterbi_states.txt

#TRUE_LABELS=`basename $TEST .txt`
#DIR_NAME=`dirname $TEST` 
#./verify.sh $DIR_NAME/${TRUE_LABELS}_true_labels.txt
