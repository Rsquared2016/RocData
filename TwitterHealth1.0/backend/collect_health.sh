#!/bin/bash

GEO_AREA=$1
CMD="run_collect_pure_python.sh $GEO_AREA m all svm_reformatted"

running=`ps -aef | grep "$CMD" | grep -v grep`
if [ ${#running} -gt 0 ]; then
    echo "Collection already running:"
    echo $running
    echo "Kill it first."
    exit
fi

nohup ./$CMD &

running=`ps -aef | grep "$CMD" | grep -v grep`
if [ ${#running} -gt 3 ]; then
    echo "`hostname`: Collection started ($CMD)"
else
    echo "`hostname`: Collection FAILED to start ($CMD)"
    exit
fi
exit
