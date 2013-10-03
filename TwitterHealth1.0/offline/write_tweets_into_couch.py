"""
python -OO write_tweets_into_couch.py words.txt log-geo-area_NYC_GPS.txt_sorted.txt_filtered_6237

"""

import sys
import couchdb
import json
import httplib
import re
import signal
import time
import traceback

from extract_features import *
from tweetReader import *
from utils import *


def printTweet(tweet):
        if tweet['lat'] != None and tweet['lon'] != None:
                print('%03.4f %03.4f | %s... | %s' % (tweet['lat'], tweet['lon'], tweet['text'][0:80], tweet['from_user']))
        else:
                print('N/A      N/A     | %s... | %s' % (tweet['text'][0:80], tweet['from_user']))





""" Read in WORDS """
WORDSfile = sys.argv[1]
(WORDS, WORDStoID) = getWORDSready(WORDSfile)

""" Init tweet reader """
reader = tweetReader(sys.argv[2])

""" Instantiate couchdb """
dbName = 'nyc_one_month'
couch = couchdb.Server('http://health.scenedipity.com:5984/')
try:
        db = couch.create(dbName) # newly created
except couchdb.http.PreconditionFailed:
        db = couch[dbName]


rexLatLon = re.compile(r'(?P<lat>[-]*[0-9]+\.[0-9]+)[^0-9-]+(?P<lon>[-]*[0-9]+\.[0-9]+)')
pNewLine = re.compile('[\r\n]+')
p = re.compile('^#*[a-z]+\'*[a-z]*$')

print "Reading file..."
while True:
        ret = reader.getNextTweet()
        if ret == None:
            break
        (tweet, tweetObj, line) = ret

        # skip tweets without any geo
        if (tweet['lat'] == None or tweet['lon'] == None):
                print "Tweet missing lat/lon"
                continue
        # remove newlines
        tweet['text'] = re.sub(pNewLine, ' ', tweet['text'])

        # classify tweet using SVM
        health = classifyTweet(tweet['text'].encode("utf-8"), p, WORDS, WORDStoID)
        tweet['health'] = health
        (id, rev) = db.save(tweet)

                


  
