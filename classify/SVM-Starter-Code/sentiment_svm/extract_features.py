import re
import sys
import time

def normalizeOrRemoveWord(w):
    p = re.compile('^#*[a-z]+\'*[a-z]*$')
    w = w.strip('.,;-:"\'?!)(').lower()
    #if w[0] == '@' or w.find('www.') != -1 or  w.find('http://') != -1 or w.find('rt',0,3) != -1:
    #if w == 'rt':
    #    continue
    if not(p.match(w)):
        return None
    return w


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

def readUniverseOfWords(fileName):
    f_words = open(fileName, 'r')
    WORDStoID = {}
    for (idx, w) in enumerate(f_words):
        if idx%100000==0 and idx>0:
            print '%d tokens read' % idx
        splitted = w.strip().split(' ')
        if len(splitted) == 1:
            WORDStoID[splitted[0]] = idx + 1
        else:
            WORDStoID[tuple(splitted)] = idx + 1
    f_words.close()
    print 'Number of distinct tokens: %d' % len(WORDStoID.keys())
    return WORDStoID

def tweetToSVMformat(text, WORDS, WORDStoID):
    # Write out SVM features
    words = filterWords(text)
    # single words
    TOKENS = set(words)
    # word pairs
    for i in range(0,len(words)-1):
        TOKENS.add( (words[i], words[i+1]) )
    # word tripples
    for i in range(0,len(words)-2):
        TOKENS.add( (words[i], words[i+1], words[i+2]) )

    svmString = '0 '    
    intersect = TOKENS.intersection(WORDS)
    features = []
    for w in intersect:
        features.append(WORDStoID[w])
    for f in sorted(features):
        svmString += ('%d:1 ' % (f))
    svmString += ('# %s\n' % (text))
    return svmString