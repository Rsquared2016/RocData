"""
server: python geod.py localhost  3 0    0 0        # chaches current day, considers current day + 3 days in the past when determining sickness
        python geod.py localhost  1 2012 7 31       # caches July 31 2012, considers current day + 1 day in the past when determining sickness
        python -OO geod.py localhost 2 2012 8 9

client:
        # get all tweets for the current day with GPS within the bounding box
        http://localhost:5000/tweets?left=-75.0&bottom=40.0&right=-72.0&top=42.6&pretty=1&limit=-1

        # get only tweets with health above a certain threshold (default health=0.2):
        http://localhost:5000/tweets?left=-75.0&bottom=40.0&right=-72.0&top=42.6&pretty=1&health=0.4

        # get up to 100 most sick tweets (sorted in descending order):
        http://localhost:5000/tweets?left=-75.0&bottom=40.0&right=-72.0&top=42.6&pretty=1&limit=100

        # submit user feedback
        python -OO geod.py localhost 2 2012 8 9
        http://localhost:5000/feedback?lon=-74.1985&lat=40.6805&userID=abc&tweetID=233597864067100673&feedback=1

        # Get health score for a bunch of tweets submitted as a JSON POST request
        curl http://166.78.236.179:5000/classify -d \
             '{"tweets": [{"id_str": "1", "text": "sick"}, {"id_str": "2", "text": "more sick"}]}'\
             -X POST --header "Content-Type: application/json; charset=UTF8"

        # Store survey results submitted as a JSON POST request to couch and index them.
        # These are accessible via /tweets request (in the 'self_reports' tag).
        curl http://166.78.236.179:5000/self_report -d \
        '{"user_id": "1a", "twitter_id": "sadilek", "geo": {"type": "Point", "coordinates": [43.154784, -77.61555599999997]}, "health": 0, "symptoms": ["Sore Throat","Fever"], "created_at": "Wed, 3 Oct 2012 13:05:11 +0000"}'\
             -X POST --header "Content-Type: application/json; charset=UTF8"

defaults:
  limit=200
  pretty=0
  health=0.2

"""

from bottle import Bottle, error, request, response, route, run
from extract_features import *
from operator import itemgetter
from pyproj import Proj
from rtree import index
from shapely.geometry import shape
from utils import calcDistanceOptimized
import couchdb
import datetime
import json
import thread
import threading
import socket
import sys

def log(s):
    print '%s: %s' % (datetime.datetime.today(), s)

def openOrCreateDb(server, name):
    server.resource.credentials = ('admin', 'admin')
    try:
        db = server.create(name) # newly created
    except couchdb.http.PreconditionFailed:
        db = server[name]
    return db

def saveObjectToCouch(db, o):
    try:
        db.save(o, batch='ok')
        return True
    except couchdb.http.ResourceConflict:
        print('Object with _id %s already in db; continuing...' % o['_id'])
        return False
    except (socket.error, couchdb.http.ServerError):
        print 'Caught error on db.save(), ignoring.'
        return False

"""
Used to record user feedback about tweet SVM classification
"""
def updateDoc(db, docID, tag, data_to_append):
    doc = db[docID]
    try:
        doc[tag].append(data_to_append)
    except KeyError:
        doc[tag] = [data_to_append]
    db.save(doc, batch='ok')
    print 'saved: %s' % doc

"""
Listen for new tweets stored in the db
"""
def listenForNewTeeets(healthThreshold, userToGPS):
    since = db.changes(feed='normal', descending=True, limit=1)['results'][0]['seq']
    changes = db.changes(feed='continuous', heartbeat='1000', include_docs=True, since=since)
    for change in changes:
        doc = change['doc']
        if doc['geo'] != None and doc['health'] >= healthThreshold and isNovelGPS(doc, userToGPS):
            (lat, lon) = doc['geo']['coordinates']
            with lock:
                tweetIdx.insert(long(doc['id_str']), (lon, lat, lon, lat), obj=doc)
            print 'Found new sick tweet:\n%s' % doc

"""
Look numDays into the past (excluding today),
retrieve all sick users (user with health >= threshold given in the by_day_sick view),
and return the set of sick users
"""
def getSickUsers(today, numDays):
    sickUsersToText = {}
    for i in xrange(1, numDays+1):
        day = today + datetime.timedelta(days=-i)
        sickUsersToTextOnDay = getSickUsersOnDay(day)
        sickUsersToText.update(sickUsersToTextOnDay)
    print 'Found %d sick users' % len(sickUsersToText.keys())
    return sickUsersToText

def getSickUsersOnDay(day):
    print 'Loading sick tweets for %s (year=%d month=%d day=%d)' % (day, day.year, day.month, day.day)
    sickUsersToText = {}
    sickTweets = db.view('Tweet/by_day_sick', key=[day.year, day.month-1, day.day], include_docs=True, reduce=False)
    print 'Found %d sick tweets' % len(sickTweets)
    for (numTweets, row) in enumerate(sickTweets):
        doc = row.doc
        sickUsersToText[doc['from_user_id']] = (doc['text'], doc['health'], doc['_id'])
    return sickUsersToText

"""
Compare the GPS of the current doc to past GPSs in userToGPS.
Return True iff the current GPS is far enough from all past GPSs.
"""
def isNovelGPS(doc, userToGPS):
    farEnough = 50 # meters
    (currLat, currLon) = doc['geo']['coordinates']
    from_user_id = doc['from_user_id']
    try:
        previousGPS = userToGPS[from_user_id]
    except KeyError:
        userToGPS[from_user_id] = [(currLat, currLon)]
        return True
    for (pastLat, pastLon) in previousGPS:
        if calcDistanceOptimized(currLat, currLon, pastLat, pastLon) < farEnough:
            return False
    userToGPS[from_user_id].append((currLat, currLon))
    return True

"""
Cache all tweets in the view with health >= healthThreshold to memory.
Furthermore, include GPS-tagged tweets from users who indicated sickness in the past n days
Our couch view uses months indexed from 0, need to subtract 1 from the actual month number!
"""
def indexTweets(year, month, day, n, healthThreshold):
    tweetIdx = index.Index()
    if year==0 and month==0 and day==0:
        today = datetime.datetime.today()-datetime.timedelta(days=1)
    else:
        today = datetime.datetime(year, month, day)
    sickUsersToText = getSickUsers(today, n)
    print 'Loading tweets for %s (year=%d month=%d day=%d)' % (today, today.year, today.month, today.day)
    todayTweets = db.view('Tweet/by_day_all_geo', key=[today.year, today.month-1, today.day], include_docs=True, reduce=False)
    print 'Found %d tweets' % len(todayTweets)
    if len(todayTweets) < 1:
        print 'No tweets found.'
        exit(-1)
    indexed = 0
    userToGPS = {}     # from_user_id -> [ (lat, lon), (lat, lon), ... ]
    nowSayingIDtoSickID = {}
    for row in todayTweets:
        doc = row.doc
        try:
            (text, health, couch_id) = sickUsersToText[doc['from_user_id']]
            doc['text'] = '%s (Now saying: %s)' % (text, doc['text'])
            doc['health'] = health
            nowSayingIDtoSickID[doc['_id']] = couch_id
        except KeyError:
            pass
        if doc['health'] >= healthThreshold and isNovelGPS(doc, userToGPS):
            (lat, lon) = doc['geo']['coordinates']
            tweetIdx.insert(long(doc['id_str']), (lon, lat, lon, lat), obj=doc)
            indexed += 1
    print '%d tweets read from %s, %d indexed (those with "health" >= %.2f)' % (len(todayTweets), db, indexed, healthThreshold)
    return (tweetIdx, nowSayingIDtoSickID, userToGPS)

"""
Cache all self reports in for a given day to memory.
Our couch view uses months indexed from 0, need to subtract 1 from the actual month number!
"""
def indexSelfReports(year, month, day):
    self_reportIdx = index.Index()
    if year==0 and month==0 and day==0:
        today = datetime.datetime.today()-datetime.timedelta(days=1)
    else:
        today = datetime.datetime(year, month, day)
    print 'Loading self reports for %s (year=%d month=%d day=%d)' % (today, today.year, today.month, today.day)
    todaySelfReports = db_self_reports.view('Survey/by_day_all_geo', key=[today.year, today.month-1, today.day], include_docs=True, reduce=False)
    print 'Found %d self reports' % len(todaySelfReports)
    return self_reportIdx

""" Calculate the area of GPS bounding box in km^2 """
def getArea(left, bottom, right, top):
    lon = (right, right, left, left)
    lat = (top, bottom, bottom, top)
    pa = Proj("+proj=aea +lat_1=%f +lat_2=%f +lat_0=%f +lon_0=%f" % (bottom, top, (bottom+top)/2.0, (left+right)/2.0))
    x, y = pa(lon, lat)
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    return shape(cop).area/1000000

""" Get the density of sick people within the obunding box """
def getAreaRisk(tweets, left, bottom, right, top):
    try:
        risk = 100 * sum([x['health'] for x in tweets]) / ((getArea(left, bottom, right, top)/areaNYC) * len(tweets))
    except ZeroDivisionError:
        risk = 0.0
    return risk

""" Get the number of sick people within X meters of the center of the bounding box """
def nearCenterRisk(tweetIdx, left, bottom, right, top):
    (centerY, centerX) = ((bottom+top)/2.0, (left+right)/2.0)
    # Find tweets within 3000m of the center
    degreesY = 30*0.000900507679 # this many degrees make up 100 meters at NYC latitude
    degreesX = 30*0.001183569359
    tweets = [n.object for n in tweetIdx.intersection((centerX-degreesX, centerY-degreesY, centerX+degreesX, centerY+degreesY), objects=True)]
    #return sum([ (x['health'] > 0.7) for x in tweets])
    return sum([ x['health'] for x in tweets])

""" Get the number of sick people within X meters of the blue dot (user_lat, user_lon) """
def nearUserRisk(tweetIdx, centerY, centerX):
    # Find tweets within 3000m of the center
    degreesY = 30*0.000900507679 # this many degrees make up 100 meters at NYC latitude
    degreesX = 30*0.001183569359
    tweets = [n.object for n in tweetIdx.intersection((centerX-degreesX, centerY-degreesY, centerX+degreesX, centerY+degreesY), objects=True)]
    #return sum([ (x['health'] > 0.7) for x in tweets])
    return sum([ x['health'] for x in tweets])

app = Bottle()
lock = threading.Lock()
# rough NYC area
areaNYC = getArea(-74.2,40.3,-73.3,40.6)

@app.route('/')
def hello():
    return "I am eager to serve annotated tweets! Hit me.\n"

"""
Receive tweets, classify health based on text, return annotated tweets
"""
@app.route('/classify', method='POST')
def classifyTweets():
    response.content_type = 'application/json; charset=UTF8'
    payload = request.json
    try:
        tweets = payload['tweets']
    except TypeError:
        print payload
        raise
    for tweet in tweets:
        tweet['health'] = classifyTweetPython(tweet['text'], p, WORDStoID, model)
        tweet['live_classified'] = True
        tweet['_id'] = tweet['id_str']
        saveObjectToCouch(db, tweet)
    return json.dumps(payload, sort_keys=True, indent=2)

"""
Receive slider+survey data, store it in couch, and index
"""
@app.route('/self_report', method='POST')
def selfReport():
    response.content_type = 'text/plain; charset=UTF8'
    doc = request.json
    lat = float(doc['geo']['coordinates'][0])
    lon = float(doc['geo']['coordinates'][1])
    doc['_id'] = '%s_%s' % (doc['user_id'], str(doc['created_at']))
    self_reportIdx.insert(long(0), (lon, lat, lon, lat), obj=doc)
    saveObjectToCouch(db_self_reports, doc)
    return 'OK'

"""
Receive user feedback on tweet classification, write it to db to the corresponding tweet, and update the cached tweets
"""
@app.route('/feedback')
def updateFeedback():
    response.content_type = 'text/plain; charset=UTF8'
    userID = request.query.userID
    tweetID = str(request.query.tweetID)
    lat = float(request.query.lat)
    lon = float(request.query.lon)
    feedback = int(request.query.feedback)
    feedbackObj = { 'user_id': userID, 'rating': feedback, 'time': datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000") }

    # See if this tweets is a "now saying:" tweet
    # If it is, update the cached "now saying" tweet and propagate feedback to the original sick tweet in db.
    # If not, add feedback to the immediate tweet in cache and in db.
    try:
        couch_id = nowSayingIDtoSickID[tweetID]
    except KeyError:
        couch_id = tweetID

    # Try to retrieve the feedbacked tweet from cache
    d = 0.000005 # float precision slack
    tweets = [n.object for n in tweetIdx.intersection((lon-d, lat-d, lon+d, lat+d), objects=True)]
    theOne = None
    for tweet in tweets:
        print tweet['_id']
        if tweet['_id'] == tweetID:
            theOne = tweet
            break
    if theOne == None:
        return 'Tweet not found'

    # Write feedback to cache
    try:
        theOne['feedback'].append(feedbackObj)
    except KeyError:
        theOne['feedback'] = [feedbackObj]
    with lock:
        tweetIdx.delete(long(tweetID), (lon, lat, lon, lat))
        tweetIdx.insert(long(tweetID), (lon, lat, lon, lat), obj=theOne)

    # Write feedback to couch
    updateDoc(db, couch_id, 'feedback', feedbackObj)
    return 'OK'

"""
Return filtered tweets in the given bounding box
"""
@app.route('/tweets')
def getTweets():
    response.content_type = 'application/json; charset=UTF8'
    left = float(request.query.left)
    bottom = float(request.query.bottom)
    right = float(request.query.right)
    top = float(request.query.top)
    pretty = request.query.pretty or '0'
    health = request.query.health or '0.2'
    health = float(health)
    limit = request.query.limit or '200'
    limit = int(limit)
    user_lat = request.query.user_lat or None
    user_lon = request.query.user_lon or None

    if user_lat != None and user_lon != None:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
        #risk = nearUserRisk(tweetIdx, user_lat, user_lon)
        risk = nearCenterRisk(tweetIdx, left, bottom, right, top)
    else:
        risk = nearCenterRisk(tweetIdx, left, bottom, right, top)
        #risk = getAreaRisk(tweets, left, bottom, right, top)

    # return tweets above $health sickness threshold
    tweets = [n.object for n in tweetIdx.intersection((left, bottom, right, top), objects=True)]
    tweets = [x for x in tweets if x['health'] >= health]
    # get top $limit most sick tweets sorted by health
    if limit == -1:
        limit = len(tweets)
    tweets = sorted(tweets, key=itemgetter('health'), reverse=True)[0 : min(limit,len(tweets))]

    self_reports = [n.object for n in self_reportIdx.intersection((left, bottom, right, top), objects=True)]

    responseJSON = {'health_risk': risk, 'num_docs': len(tweets)+len(self_reports), 'self_reports': self_reports, 'tweets': tweets}
    if pretty == '1':
        return json.dumps(responseJSON, sort_keys=True, indent=2)
    else:
        return json.dumps(responseJSON)

if __name__ == '__main__':
    hostName = sys.argv[1]
    daysInPast = int(sys.argv[2])
    year = int(sys.argv[3])
    month = int(sys.argv[4])
    day = int(sys.argv[5])
    healthThreshold = 0.2

    WORDStoID = readUniverseOfWords('words.txt')
    model = loadSVM('svm_reformatted')
    p = re.compile('^#*[a-z]+\'*[a-z]*$')

    dbName = 'm'
    couch = couchdb.Server('http://166.78.236.179:5984/')
    db = openOrCreateDb(couch, dbName)
    db_self_reports = openOrCreateDb(couch, dbName + '_self_reports')
    self_reportIdx = indexSelfReports(year, month, day)
    (tweetIdx, nowSayingIDtoSickID, userToGPS) = indexTweets(year, month, day, daysInPast, healthThreshold)

    ## This leads to significant server slow down under heavy load (or after a large number of requests has been served)
    thread.start_new_thread(listenForNewTeeets, (healthThreshold, userToGPS,))

    ## This throws libindex oduble free errors under heavy load (probably race conditions)
    #run(app, host=hostName, port=5000, debug=False, reloader=False, server='cherrypy')
    run(app, host=hostName, port=5000)
