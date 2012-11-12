# EXAMPLE:
# Use all tweets (last argument=None)
# ./run_experiment.sh data/rectangle_DateTime_greater_Seattle_2012_January_10K_uniq.txt 2012 1 1 2012 1 3 2 None None

# Use only users who have a node degree at least 3 in the meeting graph (met five distinct people during the span of the dataset), last argument=3
# ./run_experiment.sh data/rectangle_DateTime_Seattle_2012_January_August_uniq.txt      2012 3 1 2012 3 11 2 20 3

# ./run_experiment.sh data/rectangle_DateTime_NYC_2012_January_August_uniq.txt 2012 3 1 2012 3 11 2 None None

# Use only up to 100 tweets for each cell when calculating delivery time between pairs of cells
# ./run_experiment.sh data/DateTime_World_2012_10_1-2_uniq.txt 2012 10 1 2012 10 3 10 100 None

if [ "$#" -ne 10 ]; then
  echo "Unexpected # of arguments." >&2
  exit 1
fi

COSMOS_FILE=$1
YEAR_START=$2
MONTH_START=$3
DAY_START=$4
YEAR_END=$5
MONTH_END=$6
DAY_END=$7
MIN_TWEET_COUNT=$8
MAX_SAMPLE_TWEETS=$9
MIN_DEGREE=${10}

echo
echo > call_phast_for_last_experiment.bat

#./run_preprocess.sh 50 0.1 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &
./run_preprocess.sh 100  0.5 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT  $MAX_SAMPLE_TWEETS $MIN_DEGREE &
#./run_preprocess.sh 100  1 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT  $MAX_SAMPLE_TWEETS $MIN_DEGREE &
#./run_preprocess.sh 200  1 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &

#./run_preprocess.sh 100  2 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &

#./run_preprocess.sh 200  2 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &
#./run_preprocess.sh 400  1 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &
#./run_preprocess.sh 400  2 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE & 
#./run_preprocess.sh 800  2 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &
#./run_preprocess.sh 800  4 $COSMOS_FILE $YEAR_START $MONTH_START $DAY_START $YEAR_END $MONTH_END $DAY_END $MIN_TWEET_COUNT $MAX_SAMPLE_TWEETS $MIN_DEGREE &

