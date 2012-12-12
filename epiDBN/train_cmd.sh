#!/bin/bash

# [-random bool]                         Randomize the parameters {F}
# -allocateDenseCpts integer]           Automatically allocate undefined CPTs. (-1) = don't read params, (0) = don't allocate, (1) = use random initial CPT values, (2) = use uniform values {0}

NUM_OBSERVATIONS=$1
TRAIN=$2
echo $TRAIN > train.txt

echo
echo "Training..."
iters=1000
thresh=0.000001

if [ -z "$1" ]
 then
 	echo "No training file specified in arg 1"
 	exit
 fi

gmtkEMtrain -strFile dbn.str -triFile dbn.str.trifile -inputMasterFile dbn.master -inputTrainableParameters dbn_init.params -outputTrainableParameters dbn_trained.params -of1 train.txt -fmt1 ascii -nf1 0 -ni1 $NUM_OBSERVATIONS -dirichletPriors T -maxE $iters -lldp $thresh -objsNotToTrain dbn_notrain.params -allocateDenseCpts 2 -random F



# if [ -z "$1" ]
# then
#     echo "No num supplied, defaulting to training data with 1500 samples"
#     TRAIN="data/hmm_train_1500data.txt"
#     NUM="1500"
# else
#     NUM="$1"
#     TRAIN="data/hmm_train_${NUM}data.txt"
#     if [ ! -e "$TRAIN" ]
#     then
#     echo "Num not 900,1500, defaulting to training data with 1500 samples"
#     TRAIN="data/hmm_train_1500data.txt"
#     NUM="1500"
#     fi
# fi