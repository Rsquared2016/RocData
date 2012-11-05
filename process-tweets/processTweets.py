# example: python -OO processTweets.py 2000 words.txt log-geo-area_NYC_GPS_sorted_filtered_6237.dat

from tweetReader import *
from utils import *
import sys
import re

# Consider only tweets within this threshold distance from airport GPS [meters]
#dThreshold = 2000
#dThreshold = -1
dThreshold = float(sys.argv[1])

def useThisGeoTweet(tweet, foutKML):
    #foutCSV.write('%f,%f\n' % (tweet.lat, tweet.lon))
    foutKML.write('<Placemark><name>%s</name><description>%s\n%s</description><styleUrl>#hideLabel</styleUrl>\n' % (tweet.userName, tweet.text, tweet.createdAt))
    foutKML.write('<Point><coordinates>%f,%f,0</coordinates></Point></Placemark>\n' % (tweet.lon, tweet.lat))

def useThis4sqTweet(tweet, foutKML, airportCode):
    #foutCSV.write('%f,%f\n' % (tweet.lat, tweet.lon))
    lat = code2a[airportCode].lat
    lon = code2a[airportCode].lon
    foutKML.write('<Placemark><name>%s</name><description>%s\n%s</description><styleUrl>#hideLabel</styleUrl>\n' % (tweet.userName, tweet.text, tweet.createdAt))
    foutKML.write('<Point><coordinates>%f,%f,0</coordinates></Point></Placemark>\n' % (lon, lat))

def processFile(filename):
    extra = 0
    users = set() # all users that appear in this file
    print 'Processing file %s' % filename
    reader = tweetReader(filename)
    while True:
        ret = reader.getNextTweet()
        if ret == None:
            break
        (tweet, line) = ret
        users.add(tweet.userName)
        writeDataForSVM(tweet)
        
def processFile_old(filename):
    extra = 0
    users = set() # all users that appear near this airport
    airportCode = filename[-7:-4]
    print 'Processing airport %s' % airportCode
    reader = tweetReader(filename)
    #foutCSV = open(filename[:-4] + "_GPS.csv",'w')
    foutKML = open(filename[:-4] + "_GPS.kml",'w')

    foutKML.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n')
    foutKML.write('<Style id="hideLabel"><LabelStyle><scale>0</scale></LabelStyle></Style>\n')

    p1 = re.compile('\(@.*\(%s\)' % airportCode)
    p2 = re.compile('I\'m at .*\(%s\) \(' % airportCode)

    print "Reading file..."
    while True:
        ret = reader.getNextTweet()
        if ret == None:
            break
        (tweet, line) = ret

        # If dThreshold >= 0, consider only geo-tagged tweets within such radius from an airport
        # Otherwise, use all tweets
        if dThreshold >= 0:
            # First check geo tags, fall back to Foursquare mentioned in text
            if tweet.lat != None:
                d = calcDistance(tweet.lat, tweet.lon, code2a[airportCode].lat, code2a[airportCode].lon)
                if d > dThreshold:
                    continue
                useThisGeoTweet(tweet, foutKML)
                users.add(tweet.userName)
                writeDataForSVM(tweet)
            else:
                m1 = bool(p1.search(tweet.text))
                m2 = bool(p2.search(tweet.text))
                if m1 or m2: # Foursquare match found
                    #print tweet.text
                    extra += 1
                    useThis4sqTweet(tweet, foutKML, airportCode)
                    users.add(tweet.userName)
                    writeDataForSVM(tweet)
        else:
            # Use all tweets
            #useThisGeoTweet(tweet, foutKML)
            users.add(tweet.userName)
            writeDataForSVM(tweet)
        

    #foutCSV.close()
    foutKML.write('</Document></kml>')        
    foutKML.close()
    reader.printInfo()
    print 'Extra tweets mined from Foursquare checkins:', extra
    print
    return users


def calcCoocurrence():
    # How many users appear in at least 2 different airports?
    cooccur = [[0]*len(code2users.items()) for x in xrange(len(code2users.items()))]
    for (i, (airport1, users1)) in enumerate(code2users.items()):
        for (j, (airport2, users2)) in enumerate(code2users.items()):
            #if airport1 >= airport2:
            #    continue
            cooccur[i][j] = len(users1.intersection(users2))

    foutTable = open('coocurence.txt', 'w')
    #foutTable.write('   \t')
    #for a in code2users.keys():
    #    foutTable.write('%s\t' % a)
    #foutTable.write('\n')
    for (i,l) in enumerate(cooccur):
        #foutTable.write('%s\t' % code2users.keys()[i])
        for j in l:
            foutTable.write('%d\t' % j)
        foutTable.write('\n')
    foutTable.close()

    
def normalizeOrRemoveWord(w):
    w = w.strip('.,;-:"\'?!)(').lower()
    if not(p.match(w)):# and not(w[0] == '#'):
        return None
    return w


def updateUniverseOfWords(relevantTweets):
    """
    Extracts a universe of words that appear in the tweets
    """
    for tweet in relevantTweets:
        words = tweet.text.split()
        for w in words:
            w = normalizeOrRemoveWord(w)
            if w != None:
                WORDS.add(w)


def readUniverseOfWords(WORDS):
    f_words = open(sys.argv[2], 'r')
    for (idx, w) in enumerate(f_words):
        splitted = w.strip().split(' ')
        if len(splitted) == 1:
            WORDS.append(splitted[0])
        else:
            WORDS.append(tuple(splitted))
        WORDStoID[WORDS[-1]] = idx+1
    f_words.close()
    print 'Number of distinct tokens: %d' % len(WORDS)


def filterWords(text):
    """
    Keep only words that pass normalizeOrRemoveWord(), return them as a list
    """
    words = text.split()
    out = []
    for w in words:
        w = normalizeOrRemoveWord(w)
        if w != None:
            out.append(w)
    return out

            
def writeDataForSVM(tweet):
    """
    takes a list of tweet objects and writes a feature representation of each tweet on a separate line into a file
    """
    global numRelevantTweets
    # Skip retweets
    if p3.search(tweet.text) != None:
        return

    # Write plain text to a separate file
    text = tweet.text.replace("\r"," ")
    text = text.replace("\n"," ")
    #f_tweets.write('%s %d %s %s\n' % (airportCode, tweet.msgID, tweet.userName, text))
    f_tweets.write('%s\n' % (tweet.json))

    words = filterWords(tweet.text)
    # single words
    TOKENS = set(words)
    # word pairs
    for i in range(0,len(words)-1):
        TOKENS.add( (words[i], words[i+1]) )
    # word tripples
    for i in range(0,len(words)-2):
        TOKENS.add( (words[i], words[i+1], words[i+2]) )

    f_features.write('0 ')
    intersect = TOKENS.intersection(WORDS)
    features = []
    for w in intersect:
        features.append(WORDStoID[w])
    for f in sorted(features):
        f_features.write('%d:1 ' % (f))
    f_features.write('\n')
    numRelevantTweets += 1

    #f_features.write('# %s | %s | %d\n' % (airportCode, text, tweet.msgID))
        

############################################
# Main
############################################

numRelevantTweets = 0
WORDStoID = {}

p = re.compile('^#*[a-z]+\'*[a-z]*$')
p3 = re.compile('RT[^a-zA-Z0-9]')
filenames = sys.argv[3:]

WORDS = []
readUniverseOfWords(WORDS)
WORDS = frozenset(WORDS)

f_features = open('test_%s.dat' % sys.argv[2], 'w')
f_tweets = open('tweets_%s.dat' % sys.argv[2], 'w')
for f in filenames:
    processFile(f)
f_features.close()
f_tweets.close()

print 'Number of relevant tweets: %d' % numRelevantTweets

# calcCoocurrence()
