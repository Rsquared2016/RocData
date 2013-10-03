#!/bin/bash

# Forces views to get reindexed

for view in "$@"
do
	echo "Starting re-indexing of view $view"
	URL="http://166.78.236.179:5984/m/_design/Tweet/_view/${view}?update_after=true&limit=0"
	curl -X GET $URL
done
