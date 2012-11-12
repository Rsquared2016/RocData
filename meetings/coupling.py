""" Find all pairs of users that encounter each other (tweet within
DISTANCE_THRESHOLD meters of each other and within TIME_THRESHOLD
hours)
    
 (userA, userB) -> [ (lat,lon,distance,datetime), ... ] 
 where lat, lon is GPS of userA (one with smaller userID)
 
 all_tweets in the output are sorted by time
 the id of each tweet equals it's order in the output file (1 ... len(all_Tweets))
 all users that remain after filtering have their userIDs numbered 0 ... len(remaining users)
 
 
Example:  
    cache meeting data:
    python -OO coupling.py data/rectangle_DateTime_greater_Seattle_2012_January_10K_uniq.txt 2012 1 1 2012 1 3  0 0 MIN_DISTINCT_LOCATIONS 2 100 1 2

    produce KML file:
    python -OO coupling.py data/rectangle_DateTime_greater_Seattle_2012_January_10K_uniq.txt 2012 1 1 2012 1 3  1 0 MIN_DISTINCT_LOCATIONS 2 100 1 2
    
"""
 
from datetime import datetime
from rtree import index
from utils import *
import cgi
import cPickle as pickle
import colorsys
import numpy as np
import operator
import os
import rtree
import sys
import time
from Tweet import *


DEBUG = False
def log(s):
    if DEBUG==True:
        print s

def fileExists(path):
    try:
       with open(path) as f: return True 
    except IOError as e:
       return False    

def toUnix(dt):
    return int(dt.strftime('%s'))
    
"""
For a pair of users (a,b), compare the GPS of their current encounter to the past GPSs in meetingToGPS.
Return True iff the current GPS is far enough from all past GPSs.
"""
def isNovelMeeting((a,b), (currLat, currLon), meetingToGPS):
    farEnough = 200 # meters  
    try:
        previousGPS = meetingToGPS[(a,b)]
    except KeyError:
        meetingToGPS[(a,b)] = set()
        meetingToGPS[(a,b)].add((currLat, currLon))
        return True
    for (pastLat, pastLon) in previousGPS:
        if calcDistanceOptimized(currLat, currLon, pastLat, pastLon) < farEnough:
            return False
    meetingToGPS[(a,b)].add((currLat, currLon))
    return True
	
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % (round(255*rgb[2]), round(255*rgb[1]), round(255*rgb[0]))

def updateDicInc(key, value, d):
    """ Add value to the count in d[key], create this entry as [value] if it doesn't exist """
    try:
         d[key] += value
    except KeyError:
        d[key] = value
        
def updateDic(key, value, d):
    """ Add value to the list in d[key], create this entry as [value] if it doesn't exist """
    try:
         d[key].append(value)
    except KeyError:
        d[key] = [value]
        		
def readNumencounters():
    """ Read user pairs sorted by number of encounters """
    fin = open('%s/userIDs_to_numEncounters_%s_%dm_%.1fh.txt' % fileNameComponents, 'r')
    pairs = set()
    for line in fin:
        (id1, id2, numEncounters, numDistinctLocations) = line.split()
        try:
            if int(numEncounters) < MIN_NUM_ENCOUNTERS:
                continue
        except NameError:
            pass
        try:
            if int(numDistinctLocations) < MIN_DISTINCT_LOCATIONS:
                continue
        except NameError:
            pass
        pairs.add((int(id1), int(id2)))
    return pairs

def toUnix(dt):
    return int(dt.strftime('%s'))
    
def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(rgb_to_hex(colorsys.hls_to_rgb(hue, lightness, saturation)))            
    return colors
    
def writeStylesForInterestingUserPairs(interesting_pairs, foutKML):   
    colors = get_colors(len(interesting_pairs))
    for (c, pair) in enumerate(interesting_pairs):        
        foutKML.write("""
<Style id="%d_%d">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ff%s</color>
         <scale>0.5</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
""" % (pair[0], pair[1], colors[c]))        

def useThisGeoTweet(tweet1, tweet2, foutKML):
        foutKML.write('<Placemark><name>%s - %s</name><description>\n' % (tweet1.screen_name, tweet2.screen_name))
        text1 = cgi.escape(unicode(tweet1.text, 'utf-8')).encode('utf-8', 'xmlcharrefreplace')
        text2 = cgi.escape(unicode(tweet2.text, 'utf-8')).encode('utf-8', 'xmlcharrefreplace')
        foutKML.write('%s (%s)' % (text1, tweet1.dt))
        foutKML.write('\n-------------\n')
        foutKML.write('%s (%s)\n' % (text2, tweet2.dt))
        foutKML.write('</description><styleUrl>#%d_%d</styleUrl>' % (tweet1.userID, tweet2.userID))
        foutKML.write('<Point><coordinates>%f,%f,0</coordinates></Point></Placemark>\n' % (tweet1.lon, tweet1.lat))

def getTweetsNearGPSbyTimeWindow(timeWindow, tweet):
    try:
        return [n.object for n in timeWindowToGeoIdx[timeWindow].intersection((tweet.lon-(degreesX/2.0), tweet.lat-(degreesY/2.0), tweet.lon+(degreesX/2.0), tweet.lat+(degreesY/2.0)), objects=True)]
    except KeyError:
        return []

def deleteOld(timeWindow):
    try:
        del timeWindowToGeoIdx[timeWindow-2]
    except KeyError:
        return

def filterDuplicates(tweets):
    """ Remove tweets that have the same time stamp and the same location """
    nondup_tweets = []
    first = 0
    second = 1
    while second < len(tweets):
        nondup_tweets.append(tweets[first])
        (dt1, lat1, lon1) = (tweets[first].dt, tweets[first].lat, tweets[first].lon)
        try:
            (dt2, lat2, lon2) = (tweets[second].dt, tweets[second].lat, tweets[second].lon)
        except IndexError:
            break   
        while dt1==dt2 and lat1==lat2 and lon1==lon2 and second<len(tweets):
            second += 1            
            (dt2, lat2, lon2) = (tweets[second].dt, tweets[second].lat, tweets[second].lon)        
        nondup_tweets.append(tweets[second])        
        first = second + 1
        try:
            (dt1, lat1, lon1) = (tweets[first].dt, tweets[first].lat, tweets[first].lon)
        except IndexError:
            break
        while dt1==dt2 and lat1==lat2 and lon1==lon2 and first<len(tweets):            
            (dt1, lat1, lon1) = (tweets[first].dt, tweets[first].lat, tweets[first].lon)        
            first += 1            
        second = first + 1
    return nondup_tweets

def onDay(day_start_dt, day_end_dt, tweet_dt):
    if tweet_dt < day_start_dt:
        return -1
    elif day_end_dt < tweet_dt:
        return 1
    return 0

def withinUS(tweet):
    left = -126.2
    right = -61.4
    top = 49.7
    bottom = 25
    if tweet.lat<bottom or tweet.lat>top or tweet.lon<left or tweet.lon>right:
        return False
    return True
    
####################################################################################################

geoFileName = sys.argv[1]
year_s = int(sys.argv[2])
month_s = int(sys.argv[3])
day_s = int(sys.argv[4])
year_e = int(sys.argv[5])
month_e = int(sys.argv[6])
day_e = int(sys.argv[7])
use_cache = int(sys.argv[8])
lineNumStart = int(sys.argv[9]) # start with this line number (0=start from the beginning)
#assert(sys.argv[10] == MIN_DISTINCT_LOCATIONS)
assert(sys.argv[11] == 2)
DISTANCE_THRESHOLD = int(sys.argv[12]) # meters
TIME_THRESHOLD = float(sys.argv[13]) # hours
MIN_TWEET_COUNT = int(sys.argv[14]) # process only users with more than MIN_TWEET_COUNT tweets in the given time period

degreesY = DISTANCE_THRESHOLD * 0.00000900507679 # this many degrees make up 1 meter at NYC latitude
degreesX = DISTANCE_THRESHOLD * 0.00001183569359

if sys.argv[10] == 'MIN_NUM_ENCOUNTERS':
    MIN_NUM_ENCOUNTERS = int(sys.argv[11]) # consider only pairs of people who meet at least this many times
elif sys.argv[10] == 'MIN_DISTINCT_LOCATIONS':
    MIN_DISTINCT_LOCATIONS = int(sys.argv[11]) # consider only pairs of people who meet at at least least this many DIFFERENT places
else:
    print 'Unexpected parameter: %s' % sys.argv[10]
    exit(-1)

day_start_dt = datetime(year_s, month_s, day_s)
day_end_dt = datetime(year_e, month_e, day_e)
print 'Start datetime: %s' % day_start_dt
print 'End   datetime: %s' % day_end_dt
    
baseDir = os.path.dirname(geoFileName)
geoBaseName = os.path.splitext(os.path.basename(geoFileName))[0]
fileNameComponents = (baseDir, geoBaseName, DISTANCE_THRESHOLD, TIME_THRESHOLD)

geoFile = open(geoFileName, 'r')
timeWindowToGeoIdx = {} # 3 -> geo index with tweets that hash to the third TIME_THRESHOLD time window of the dataset
all_tweets = []
lastLat = -1
lastLon = -1
lastDt = -1
duplicates = 0
userToTweetCount = {}
for (lineNum, line) in enumerate(geoFile):
    try:
        (dt, userID, screen_name, lat, lon, text) = line.split('\t', 5)
    except ValueError:
        (dt, userID, lat, lon) = line.split('\t')
        screen_name = None
        text = None
    if lat==lastLat and lon==lastLon and dt==lastDt:
        duplicates += 1
        continue    
    lastLat = lat
    lastLon = lon
    lastDt = dt
    tweet = Tweet(lineNum, dt, userID, screen_name, lat, lon, text)
    if not(withinUS(tweet)):
        continue
    # Get only the time window we care about 
    tweetTimeRelevance = onDay(day_start_dt, day_end_dt, tweet.dt)
    if tweetTimeRelevance == -1:
        continue # tweet too old for this day
    elif tweetTimeRelevance == 1:
        break # tweet too new for this day   
        
    updateDicInc(tweet.userID, 1, userToTweetCount)
    all_tweets.append(tweet)    
    if lineNum % 100000 == 0:
        print '%s lines done' % lineNum
geoFile.close()
print 'Geo data read.'
print '%d lines read' % (lineNum+1)
#all_tweets = filterDuplicates(all_tweets)
print 'Duplicate tweets: %d' % duplicates
print 'Unique tweets: %d' % (len(all_tweets))

# Remove tweets from users who tweet too infrequently
pickle.dump(userToTweetCount, open('%s/userToTweetCount_%s_%dm_%.1fh.pickle' % fileNameComponents, 'wb'), -1)
#for (userID, numTweets) in sorted(userToTweetCount.iteritems(), key=operator.itemgetter(1), reverse=False):
#    print userID, numTweets   
keepUsers = set()
for (userID, numTweets) in userToTweetCount.items():
    if numTweets > MIN_TWEET_COUNT:
        keepUsers.add(userID)
del userToTweetCount

userToMonotonicID = {}
for (id, user) in enumerate(keepUsers):
    userToMonotonicID[user] = id

# Make sure all tweets have sequential IDs and users are sequential as well
new_all_tweets = []
newTweetID = 1
for tweet in all_tweets:
    if tweet.userID in keepUsers:
        tweet.tweetID = newTweetID
        tweet.userID = userToMonotonicID[tweet.userID]
        newTweetID += 1
        new_all_tweets.append(tweet)
all_tweets = new_all_tweets
print 'Unique tweets for users who tweet at least %dx: %d' % (MIN_TWEET_COUNT, len(all_tweets))

# Prepare time windows with coresponding tweeets
for tweet in all_tweets:
    timeWindow = toUnix(tweet.dt) / int(TIME_THRESHOLD * 3600)
    try:
        timeWindowToGeoIdx[timeWindow].insert(long(lineNum), (tweet.lon, tweet.lat, tweet.lon, tweet.lat), obj=tweet)
    except KeyError:
        timeWindowToGeoIdx[timeWindow] = index.Index()
        timeWindowToGeoIdx[timeWindow].insert(long(lineNum), (tweet.lon, tweet.lat, tweet.lon, tweet.lat), obj=tweet)
        
if use_cache == 0:
    # read meeting data from scratch 
    interesting_pairs = set()
elif use_cache == 1:
    print 'Using cached meeting data.'
    interesting_pairs = readNumencounters()
    print 'Interesting pairs read.'
else:
    print 'Incorrect cache argument'
    exit(-1)

#foutRoute = open('%s/routing_%s.txt' % (baseDir, geoBaseName), 'w')
foutKML = open("%s/couplings_%s_%dm_%.1fh.kml" % fileNameComponents, 'w')
foutKML.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n')
foutKML.write('<Style id="hideLabel"><LabelStyle><scale>0</scale></LabelStyle></Style>\n')
if use_cache == 1:
    writeStylesForInterestingUserPairs(interesting_pairs, foutKML)
foutKML.write("""
<Style id="randomColorIcon">
      <LabelStyle><scale>0</scale></LabelStyle>
      <IconStyle>
         <color>ffffffff</color>
         <colorMode>random</colorMode>
         <scale>1</scale>
         <Icon>
            <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
         </Icon>
      </IconStyle>
</Style>
""")

# Iterate through all geo tweets and find encounters
encounters = 0
#kml_pins = 0
#coupling = {} # (user1ID, user2ID) -> # of meetings
#meetingToGPS = {} # (user1ID, user2ID) -> set of distinct (far apart enough) meeting GPS
routing_opportunities = [] # list of tuples, where each tuple represents an instance of potential package exchange
for (i, tweet) in enumerate(all_tweets):    
    # Get tweet geo index from this hour, previous hour, and next hour (each only if it exists)
    timeWindow = toUnix(tweet.dt) / int(TIME_THRESHOLD * 3600)
    nearby_tweets = getTweetsNearGPSbyTimeWindow(timeWindow, tweet)
    nearby_tweets.extend(getTweetsNearGPSbyTimeWindow(timeWindow-1, tweet))
    nearby_tweets.extend(getTweetsNearGPSbyTimeWindow(timeWindow+1, tweet))
    deleteOld(timeWindow)    
    for nearby_tweet in nearby_tweets:
        if tweet.userID == nearby_tweet.userID:
            continue   
        delta_t = abs((tweet.dt - nearby_tweet.dt).total_seconds()) / 3600.0       
        if delta_t >= TIME_THRESHOLD:
            continue
         
        # Make sure t1 always has smaller userID than t2       
        if tweet.userID > nearby_tweet.userID:
            t1 = nearby_tweet
            t2 = tweet
        else:
            t1 = tweet
            t2 = nearby_tweet                                  
        
        # update distinct meeting place count
        if use_cache == 0:
            # try:
                # coupling[(t1.userID, t2.userID)] += 1
            # except KeyError:
                # coupling[(t1.userID, t2.userID)] = 1
            #isNovelMeeting((t1.userID, t2.userID), (np.mean([t1.lat,t2.lat]), np.mean([t1.lon,t2.lon])), meetingToGPS)
            routing_opportunities.append((t1.userID, t2.userID, t1.tweetID, t2.tweetID, t1.lat, t1.lon, t1.dt, t2.lat, t2.lon, t2.dt))
        
        # if use_cache == 1:
            # if (t1.userID, t2.userID) in interesting_pairs:
                # useThisGeoTweet(t1, t2, foutKML)
                # kml_pins += 1
        encounters += 1
        
        #log('%d %d: %f %f %s' % (t1.userID, t2.userID, t1.lat, t1.lon, t1.dt))
        #log('     %f %f %s' % (t2.lat, t2.lon, t2.dt))        
    if i%10000 == 0:
        print '%.2f%% done.' % (float(i)/lineNum*100)
foutKML.write('</Document></kml>')      
foutKML.close()
if use_cache == 0:
    pickle.dump(routing_opportunities, open('%s/routing_opportunities_%s_%dm_%.1fh.pickle' % fileNameComponents, 'wb'), -1)
    # Dump all_tweets, but only if the file does not exist, or is more than 5 minutes old
    fileName = '%s/all_tweets_%s.pickle' % (baseDir, geoBaseName)    
    if fileExists(fileName):
        fileModifiedTime = datetime.fromtimestamp(os.path.getmtime(fileName))
        print "Modification time:",fileModifiedTime 
        if abs(toUnix(fileModifiedTime) - toUnix(datetime.now())) > 60*5:
            print 'Writing all_tweets* because the file may be stale...'
            pickle.dump(all_tweets, open(fileName, 'wb'), -1)
    else:
        print 'Writing all_tweets* because the file does not exist...'
        pickle.dump(all_tweets, open(fileName, 'wb'), -1)
    #fout = open('%s/all_tweets_%s.txt' % (baseDir, geoBaseName), 'w')
    #for tweet in all_tweets:
    #    fout.write('%s\t%d\t%f\t%f\n' % (datetime.strftime(tweet.dt, "%m/%d/%Y %I:%M:%S %p"), tweet.userID, tweet.lat, tweet.lon))
    #fout.close()
exit()
    
    
    
    
    
# Write out processed meeting data
if use_cache == 0:
    fout_couples = open('%s/userIDs_to_numEncounters_%s_%dm_%.1fh.txt' % fileNameComponents, 'w')
    for (users, numMeetings) in sorted(coupling.iteritems(), key=operator.itemgetter(1), reverse=True):
        fout_couples.write('%d %d %d %d\n' % (users[0], users[1], numMeetings, len(meetingToGPS[users])))
    fout_couples.close()
    print 'Encounters found: %d' % encounters
    print 'KML pins written: %d' % kml_pins
if use_cache==0 or len(interesting_pairs) == 0:
    print """
    #######################################################
    #  WARNING: This run was only to cache meeting data,  #
    #  run again with 1 0 arguments to get new KML file   # 
    #######################################################
    """
