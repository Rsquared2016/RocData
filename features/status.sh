#!/bin/bash

echo "Last 10 lines:"
tail -n 10 "$1"

#if [ "$1" = "meetings.log" ]; then
#    echo "Recent positives:"
#    set $res = $( tail -n 100 "$1" | grep YES )
#    if [ "$res" = "" ]; then
#        echo -e "\tNo recent positive examples found :("
#    fi
#fi