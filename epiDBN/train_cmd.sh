#!/bin/bash

NUM_OBSERVATIONS=$1
TRAIN=$2
echo $TRAIN > train.txt

echo
echo "Training..."
iters=5 #1000
thresh=0.000001

if [ -z "$1" ]
 then
 	echo "No training file specified in arg 1"
 	exit
 fi

CMD="gmtkEMtrain -strFile dbn.str -cmbeam 0.5 -triFile dbn.str.trifile -inputMasterFile dbn.master -inputTrainableParameters dbn_init.params -outputTrainableParameters dbn_trained.params -of1 train.txt -fmt1 ascii -nf1 0 -ni1 $NUM_OBSERVATIONS -dirichletPriors T -maxE $iters -lldp $thresh -objsNotToTrain dbn_notrain.params -allocateDenseCpts 2 -random F"

echo $CMD
$CMD
