#!/bin/bash

# Downloads a selected day from a dataset of geo-tagged tweets that includes 100km around the following metros:
# London, LA, Boston, NYC, Seattle, SF

YEAR=$1
MONTH=$2
DAY=$3

URL="http://fount.in:5984/m/_design/Tweet/_view/by_day_all_geo?key=%5B${YEAR},`expr ${MONTH} - 1`,${DAY}%5D&include_docs=True"
echo $URL
curl -X GET $URL
