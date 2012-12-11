"""
    observe_health.py <db-name> <file-path> [<health-split>]

    example:
        python observe_health.py airport_toy health.txt 0.8
"""

import couchdb
from datetime import datetime, timedelta
import logging
import operator
import sys

def key_to_datetime(key):
    return datetime(key[1], key[2], key[3])

def updateDic(key, value, d):
    """ Add value to the count in d[key], create this entry as [value] if it doesn't exist """
    try:
        d[key] += value
    except KeyError:
        d[key] = value

def updateUserToDailyHealth(user, date, health_score, d):
    """ If health_score is greater than current score stored for user, overwrite it """
    try:
        d[(user, date)] = max(d[(user, date)], health_score)
    except KeyError:
        d[(user, date)] = health_score


""" start logging module """
logging.basicConfig(filename = 'observe_health.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" grab cmdline args and initialize parameters """
db_name = sys.argv[1]
file_name = sys.argv[2]
health_split = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.8
time_slices = set()
users = set()
activeUsers = set()
userToNumTweets = {}
userToDailyHealth = {} # { (userID, datetime): maxHealthScoreOverDatetime, ... } 
# if we don't include this, we get stuff from like august 2011...
start_date = datetime(2012, 12, 1)
end_date = start_date
min_tweet_count = 7 # don't include users who tweeted fewer times than min_tweet_count

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" grab all rows """
results = db.view("Tweet/max_health_score", reduce = True, group = True)
print "Tweets read from view: %d" % len(results)
for row in results:
    user, date, score = row.key[0], key_to_datetime(row.key), row.value
    end_date = max(end_date, date)
    # skip REALLY old tweets
    if date < start_date:
        continue
    #print "[%s] %s @ %s" % (user, score, date)
    updateUserToDailyHealth(user, date, score, userToDailyHealth)
    updateDic(user, 1, userToNumTweets)
    users.add(user)
    time_slices.add(date)
    
""" Print histogram of tweet count over users """
logging.debug('Active users: (id: count)')
for (userID, numTweets) in sorted(userToNumTweets.iteritems(), key=operator.itemgetter(1), reverse=True):
    if numTweets < min_tweet_count:
        break
    activeUsers.add(userID)
    logging.debug('%s: %d' % (userID, numTweets))

print "Found %d days in the db (%s - %s)." % ((end_date-start_date).days, start_date, end_date)
print "Found %d active users who tweeted >=%d times (out of %d (%.2f%%))" % (len(activeUsers), min_tweet_count, len(users), float(len(activeUsers))/len(users)*100)

print "Writing time indices and health observations for all users over every day..."
""" dump observations to specified file """
with open(file_name, 'w+') as obs_file:
    # Header
    obs_file.write('%% TIME_STEP ')
    for user in sorted(activeUsers):
        obs_file.write('%s ' % user)
    obs_file.write('\n')

    # Observations: TIME_STEP + user health states (1=user tweeted something sick on a given day, 0=all his tweets were healthy during the day, 2=no tweet)
    last_time_slice = start_date + timedelta(days=-1)
    for (t, time_slice) in enumerate(sorted(time_slices)):
        if (time_slice-last_time_slice).days != 1:
            print "Seems we're missing user observations: jump %s -> %s. Terminating" % (last_time_slice, time_slice)
            exit(-1)
        obs_file.write('%d ' % t) # Write time index as the first observation on each line
        for user in sorted(activeUsers):
            try:
                score = userToDailyHealth[(user, time_slice)]
                health_state = 1 if score >= health_split else 0
            except KeyError:
                health_state = 2        
            obs_file.write('%d ' % health_state)
        obs_file.write('\n')
        last_time_slice = time_slice

print "Finished writing data to %s" % file_name
logging.debug('Done! Exiting...')

