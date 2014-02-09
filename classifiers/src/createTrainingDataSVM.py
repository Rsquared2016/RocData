# Prepares training data for SVMlight from labeled tweets
# Outputs svm_model/sys.argv[1].words file with all the unique tokens that appear in the training data
# Outputs train.dat file, where each line contains tweet's class, representation of a tweet in the feature space defined by the presence of a token word, #, and the name of the class
# For example:
#  -1 1175:1 1550:1 1859:1 1874:1 2872:1 3104:1 3488:1 3562:1 3853:1 4030:1 5637:1 6295:1 6679:1 6935:1 6942:1 7152:1 9016:1 # no

# Run: 
# python -OO createTrainingDataSVM.py training_data.txt 1 

import os
import re
import sys
from operator import itemgetter
from extract_features import *

def updateCount(w, tmp):
    try:
        tmp[w] += 1
    except KeyError:
        tmp[w] = 1


def updateUniverseOfWords(tweets):
    """
    Extracts a universe of words that appear in the tweets
    """
    tmp = {}
    for tweet in tweets:
        for w in filterWords(tweet):
            updateCount(w, tmp)
    for (w, count) in sorted(tmp.items(), reverse=True, key=itemgetter(1)):
        if count < countThreshold:
            break
        WORDS.add(w)


def updateUniverseOfWordPairs(tweets):
    """
    Extracts a universe of word pairs that appear in the tweets
    """
    tmp = {}
    for tweet in tweets:
        words = filterWords(tweet)
        for i in range(0,len(words)-1):
            updateCount((words[i], words[i+1]), tmp)
    for (w, count) in sorted(tmp.items(), reverse=True, key=itemgetter(1)):
        if count < countThreshold:
            break
        WORDPAIRS.add(w)


def updateUniverseOfWordTripples(tweets):
    """
    Extracts a universe of word tripples that appear in the tweets
    """
    tmp = {}
    for tweet in tweets:
        words = filterWords(tweet)
        for i in range(0,len(words)-2):
            updateCount((words[i], words[i+1], words[i+2]), tmp)
    for (w, count) in sorted(tmp.items(), reverse=True, key=itemgetter(1)):
        if count < countThreshold:
            break
        WORDTRIPLES.add(w)




# Consider only tokens that appear at least countThreshold times
countThreshold = int(sys.argv[2])

log = open(sys.argv[1], 'r')
filePrefix = os.path.splitext(os.path.basename(sys.argv[1]))[0]

ids = []
tags = []
tags_set = set()
tagToCount = {}
texts = []

for line in log:
    (id, tag, text) = line.split(' ', 2)
    ids.append(int(id))
    tags.append(tag)
    tags_set.add(tag)
    texts.append(text)
log.close()

print 'Universe of tags: %s' % tags_set

for t in tags:
    try:
        tagToCount[t] += 1
    except KeyError:
        tagToCount[t] = 1

print tagToCount


# Extract SVM training data

# Collect and write out all words
WORDS = set()
WORDPAIRS = set()
WORDTRIPLES = set()
updateUniverseOfWords(texts)
print 'Number of distinct words: %d' % len(WORDS)
updateUniverseOfWordPairs(texts)
print 'Number of distinct word pairs: %d' % len(WORDPAIRS)
updateUniverseOfWordTripples(texts)
print 'Number of distinct word tripples: %d' % len(WORDTRIPLES)
WORDS = list(WORDS)
WORDPAIRS = list(WORDPAIRS)
WORDTRIPLES = list(WORDTRIPLES)
WORDStoID = {} # mapping of all tokens to IDs
ID = 1

#print WORDS

fout_w = open('svm_model/%s.words' % filePrefix, 'w')
for w in WORDS:
    fout_w.write(w+'\n')
    WORDStoID[w] = ID
    ID += 1
ALLWORDS = set(WORDS)
WORDS = None

for (w1, w2) in WORDPAIRS:
    fout_w.write('%s %s\n' % (w1, w2))
    WORDStoID[(w1, w2)] = ID
    ID += 1
ALLWORDS.update(WORDPAIRS)
WORDPAIRS = None

for (w1, w2, w3) in WORDTRIPLES:
    fout_w.write('%s %s %s\n' % (w1, w2, w3))
    WORDStoID[(w1, w2, w3)] = ID
    ID += 1
ALLWORDS.update(WORDTRIPLES)
WORDTRIPLES = None

fout_w.close()

positive = 0
negative = 0
fout = open('svm_model/%s.dat' % filePrefix, 'w')
for (i, tag) in enumerate(tags):
    if i%50000 == 0:
        percent = int(round(float(i)/len(tags)*100))
        print '%d%% done' % percent
    # determine label (health-related vs. everything else in english)
    #if tag=="health" or tag=="sick":
    if tag=="sick":
        fout.write('1 ')
        positive += 1
    elif tag=="no" or tag=="health" or tag=="notenglish":
        fout.write('-1 ')
        negative += 1
    else:
        continue

    words = filterWords(texts[i])
    # single words
    TOKENS = set(words)
    # word pairs
    for i in range(0,len(words)-1):
        TOKENS.add( (words[i], words[i+1]) )
    # word tripples
    for i in range(0,len(words)-2):
        TOKENS.add( (words[i], words[i+1], words[i+2]) )

    intersect = TOKENS.intersection(ALLWORDS)
    features = []
    for w in intersect:
        features.append(WORDStoID[w])
    for f in sorted(features):
        fout.write('%d:1 ' % (f))
    fout.write('\n')
fout.close()

print '# positives (sick): %d' % positive
print '# negatives (all other):      %d' % negative
