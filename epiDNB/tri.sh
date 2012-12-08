#!/usr/bin/env bash

#TRIANGULATION="completeframeleft"
rm -rf hmm.str.trifile
gmtkTriangulate -str hmm.str -inputM hmm.mtr #-tri $TRIANGULATION
#gmtkTriangulate -str model.str -inputM model.mtr -tri S50W10
