#!/bin/bash

# Example: ./verify.sh data/hmm_test_15000_true_labels.txt 

NUM=$(grep -c 'X([[:digit:]]*)=' hmm_vitVals.txt)
egrep -o '=[0-9]+ hidden' hmm_vitVals.txt | egrep -o '[0-9]+' > viterbi_states.txt
MISSES=$(diff viterbi_states.txt $1 | grep -c '<')
echo "Correctly identified $((NUM-MISSES)) of $NUM data points"