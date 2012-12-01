import numpy
import re
import sys
import time

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

def normalizeOrRemoveWord(w, p):
    w = w.strip('.,;-:"\'?!)(').lower()
    if not(p.match(w)):# and not(w[0] == '#'):
        return None
    return w

def filterWords(text, p):
    """
    Keep only words that pass normalizeOrRemoveWord(), return them as a list
    """
    words = text.split()
    out = []
    for w in words:
        w = normalizeOrRemoveWord(w, p)
        if w != None:
            out.append(w)
    return out

##############################################################

def loadSVM(fileName):
    f_model = open(fileName, 'r')
    lines = f_model.readlines()
    f_model.close()
    D = int(lines[0])
    b = float(lines[1])
    alphaY = float(lines[2])
    featureWeights = lines[3].strip().split(' ')
    model = numpy.zeros(D)
    assert(len(model) > 0)
    for f in featureWeights:
        (num, w) = f.split(':')
        model[int(num)] = float(w)
    return model

def classifyTweetPython(text, p, WORDStoID, model):
    # Transform text into SVM feature space
    words = filterWords(text, p)
    # single words
    TOKENS = set(words)
    # word pairs
    for i in xrange(0,len(words)-1):
        TOKENS.add( (words[i], words[i+1]) )
    # word tripples
    for i in xrange(0,len(words)-2):
        TOKENS.add( (words[i], words[i+1], words[i+2]) )

    score = 0
    for word in TOKENS:
        try:
            word_id = WORDStoID[word]
        except KeyError:
            continue
        score += model[word_id]
        #print '%.4f: %s = %d' % (score, word, word_id)
    return score