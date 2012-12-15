"""
    health.py <db-name> <pickle-file-path> <health-split> <start-date> <end-date>

    example:
        python health.py airport_toy health_toy.pickle 0.8 2012-11-17 2012-12-9
"""

import couchdb
import cPickle as pickle
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
logging.basicConfig(filename = 'health.log', level = logging.DEBUG, filemode = 'w', format='%(message)s')

""" grab cmdline args and initialize parameters """
db_name = sys.argv[1]
file_name = sys.argv[2]
health_split = float(sys.argv[3])
dt = [int(d) for d in sys.argv[4].split('-')]
start_date = datetime(dt[0], dt[1], dt[2])
dt = [int(d) for d in sys.argv[5].split('-')]
end_date = datetime(dt[0], dt[1], dt[2])
min_tweet_count = 5 # don't include users who tweeted fewer times than min_tweet_count

time_slices = set()
users = set()
activeUsers = set()
userToNumTweets = {}
userToDailyHealth = {} # { (userID, datetime): maxHealthScoreOverDatetime, ... } 

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db = couch[db_name]

""" grab all rows """
results = db.view("Tweet/max_health_score", reduce = True, group = True)
print "Tweets read from view: %d" % len(results)
for row in results:
    user, date, score = int(row.key[0]), key_to_datetime(row.key), row.value
    if date < start_date or date > end_date:
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
    logging.debug('%d: %d' % (userID, numTweets))

if (end_date-start_date).days+1 > len(time_slices):
    print 'Not all requested days found in db.'
    exit(-1)

print "Using %d days from the db (%s - %s)." % (len(time_slices), start_date, end_date)
print "Found %d active users who tweeted >=%d times (out of %d (%.2f%%))" % (len(activeUsers), min_tweet_count, len(users), float(len(activeUsers))/len(users)*100)

""" merge observations into a coherent structure """
health = {} # { datetime: {userID: 0-2, ...}, ... }
# Organized users
activeUsersList = sorted(list(activeUsers))

for (t, time_slice) in enumerate(sorted(time_slices)):
    health[time_slice] = {}
    for user in activeUsersList:
        try:
            score = userToDailyHealth[(user, time_slice)]
            health_state = 1 if score >= health_split else 0
        except KeyError:
            health_state = 2
        health[time_slice][user] = health_state

with open(file_name, 'wb') as pfile:
    pickle.dump(health, pfile, -1)
print "Finished writing data to %s" % file_name
logging.debug('Done! Exiting...')

