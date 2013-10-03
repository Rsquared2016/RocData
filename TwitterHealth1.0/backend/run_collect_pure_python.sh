#!/bin/bash

GEO_AREA=$1
DB_NAME=$2
GEO=$3
SVM_MODEL_FILE=$4

echo Geo area: $GEO_AREA
echo Geo option: $GEO
echo DB name: $DB_NAME
echo SVM model file: $SVM_MODEL_FILE

export PYTHONPATH=/u/sadilek/code/lib/python
python -OO collect_tweets.py words.txt 3 $GEO_AREA $DB_NAME $GEO $SVM_MODEL_FILE
