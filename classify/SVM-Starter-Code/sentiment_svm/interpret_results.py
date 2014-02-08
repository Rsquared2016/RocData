# Takes prediction made by an SVM, and a file with the corresponding tweets
# Outputs:
#  - list of usernames that appeared sick at least once (one tweet)
#  - pickled mapping from time segment to usernames that are sick in that time segment
#    (animateSickUsers.py can then be used to animate the segments of sick users)
#  - histogram of the scores

# Example: 
# python -OO interpret_results.py predictions_svm ../nyc.trim.sort 0.8

import sys
import re
from collections import Counter
from tweetReader import *
from utils import *

def updateSegmentToSick(segNum, userName):
      global segmentToSick
      try:
            segmentToSick[segNum].add(tweet.userName)
      except KeyError:
            segmentToSick[segNum] = set(tweet.userName)
      
            
p3 = re.compile('RT[^a-zA-Z0-9]')

f_preds = open(sys.argv[1], 'r')
reader = tweetReader(sys.argv[2])
THRESHOLD = float(sys.argv[3])

#fout = open('interpretation.txt', 'w')
fout_train = open('labeled_sick_%g.txt' % THRESHOLD, 'w')
f_sick_users = open('sick_users_%s' % sys.argv[1], 'w')
sick_users = set()

# Load predicted scores
scores = []
for p in f_preds:
      scores.append(float(p.strip()))
f_preds.close()

# For NYC dataset
INTERVAL = 24*3600 # Model with this granularity (seconds)
#START = 1274241600 # Wed May 19 2010 00:00:00 GMT-4
#END = 1277078400 # Sun Jun 20 2010 00:00:00 GMT-4
START = 1274227200 # Wed, 19 May 2010 00:00:00 GMT
END = 1276992000 # Sun, 20 Jun 2010 00:00:00 GMT
daySegments = range(START, END+1, INTERVAL)
daySegmentsPairs = []
for i in range(0,len(daySegments)-1):
      daySegmentsPairs.append((datetime.fromtimestamp(daySegments[i]+1), datetime.fromtimestamp(daySegments[i+1])))
      print 'Segment %d: %s -> %s' % (i, daySegmentsPairs[-1][0], daySegmentsPairs[-1][1])

segmentToSick = {}
segmentNumOld = 0
lineNum = 0
while True:
      ret = reader.getNextTweet()
      if ret == None:
            break
      (tweet, line) = ret
      (human_time, unix_time) = getTime(tweet.createdAt)
      if unix_time < START:
            lineNum += 1
            continue
      segmentNum = (unix_time-START)/INTERVAL
      if segmentNum != segmentNumOld:
            segmentNumOld = segmentNum
      
      #print human_time, unix_time, tweet.createdAt
      t = tweet.text.strip()
      t = t.replace("[\r\n]+"," ")
      if THRESHOLD >= 0: #focus on health-related tweets
            if scores[lineNum] > THRESHOLD:
                  print '%+.2f %s' % (scores[lineNum] , t)
                  updateSegmentToSick(segmentNum, tweet.userName)
                  fout_train.write('%.3f %s\n' % (scores[lineNum], t))
                  #fout_train.write('0 health %s\n' % (t.strip()))
                  sick_users.add(tweet.userName)
            #fout.write('%+.4f %s\n' % (scores[lineNum] , t))
      else: # focus on all other tweets
            if scores[lineNum] < THRESHOLD: #-0.75
                  if p3.search(t) == None:
                        print '%+.2f %s' % (scores[lineNum] , t)
                        #fout_train.write('0 no %s\n' % (t.strip()))
            #fout.write('%+.4f %s\n' % (scores[lineNum] , t))
      lineNum += 1

#fout.close()
fout_train.close()

import pickle
pickle.dump( segmentToSick, open( 'segmentToSick_%g-reproduce.pickle' % THRESHOLD, "wb" ) )

for u in sorted(sick_users):
      f_sick_users.write(u + '\n')
f_sick_users.close()

scores_round = []
for s in scores:
      scores_round.append(round(s,1))
      
histogram = Counter(scores_round)
for b in sorted(histogram.keys()):
      print '%+.1f: %d' % (b, histogram[b])
      
print 'Minimum score %.4f' % min(scores)
print 'Maximum score %.4f' % max(scores)

reader.printInfo()
