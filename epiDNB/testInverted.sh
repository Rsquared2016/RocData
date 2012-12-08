#!/bin/bash
gmtkViterbi -strFile model.str \
    -triFile model.str.trifile \
    -of1 $FILE1 -fmt1 $FILETYPE -ni1 0 -nf1 2 \
    -of2 $FILE2 -fmt2 $FILETYPE -ni2 2 -nf2 0 \
    -fdiffact2 rl \
    -inputMasterFile model.mtr \
    -inputTrainableParameters trained.params \
    -vitValsFile $LOGDIR/vitVals-sid$sid.txt \
    -verbosity $VERB \
    2>&1 | tee $OUTPUT
