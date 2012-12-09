"""
    observe_health.py <file-path> [<health-split>]
"""

import couchdb
from datetime import datetime, timedelta
import sys

def key_to_datetime(key):
    return datetime(key[1], key[2], key[3])

""" grab cmdline args and initialize parameters """
file_name = sys.argv[1]
health_split = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.8
time_slices = {}
fill_slices = {}
users = []
# if we don't include this, we get stuff from like august 2011...
start_date = datetime(2012, 11, 15)

""" initialize couchdb """
couch = couchdb.Server('http://dev.fount.in:5984')
couch.resource.credentials = ('admin', 'admin')
db_airports = couch['airport_tweets']

""" grab all rows """
results = db_airports.view("Tweet/max_health_score", reduce = True, group = True, stale = 'update_after')
print "Got %s rows." % len(results)
for row in results:
    user, date, score = row.key[0], key_to_datetime(row.key), row.value
    # skip REALLY old tweets
    if date < start_date:
        continue
    print "[%s] %s @ %s" % (user, score, date)
    if not user in users:
        users.append(user)
    if not date in time_slices:
        time_slices[date] = []
    sick = 1 if score >= health_split else 0
    time_slices[date].append((user, sick))

""" fill in timeslices where user was missing """
for date, pairs in time_slices.items():
    users_today = [p[0] for p in pairs]
    for user in users:
        if not user in users_today:
            if not date in fill_slices:
                fill_slices[date] = []
            fill_slices[date].append((user, 2))

for date, pairs in fill_slices.items():
    time_slices[date].extend(pairs)
    time_slices[date].sort(key = lambda pair: pair[0])
users.sort()

print "Writing health observations for all users over every day..."
""" dump observations to specified file """
with open(file_name, 'w+') as obs_file:
    output = ["%s\n" % " ".join(users)]
    observations = []
    for date, pairs in sorted(time_slices.items()):
        if len(pairs) != len(users):
            print "Seems we're missing user observations for %s..." % date
        states = [str(p[1]) for p in pairs]
        # for debugging purposes!
        #observations.append("%s\n" % date)
        observations.append(" ".join(states) + "\n")
    output.extend(observations)
    obs_file.writelines(output)
print "Finished writing data to %s" % file_name
print "# Users: %s" % len(users)
