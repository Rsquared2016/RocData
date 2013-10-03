# Transforms the textual representation of a list of tweets into the feature space of the SVM
# example: python extract_features.py words.txt test.txt
# outputs test.dat (sys.argv[2][:-3]+'dat') that can be fed to svm_perf_classify

import re
import socket
import sys
import time

def createSocket():
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = './svm_socket_offline'
    #print >>sys.stderr, 'connecting to %s' % server_address
    while True:
        try:
            sock.connect(server_address)
            return sock
        except socket.error, msg:
            print >>sys.stderr, msg
            time.sleep(1)
    

def readUniverseOfWords(WORDS, WORDStoID):
    f_words = open(sys.argv[1], 'r')
    for (idx, w) in enumerate(f_words):
        if idx%100000==0 and idx>0:
            print '%d tokens read' % idx
            #print 'sleeping for 20 seconds'
            #time.sleep(20)
        splitted = w.strip().split(' ')
        if len(splitted) == 1:
            WORDS.append(splitted[0])
        else:
            WORDS.append(tuple(splitted))
        WORDStoID[WORDS[-1]] = idx+1
    f_words.close()
    print 'Number of distinct tokens: %d' % len(WORDS)

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

def getWORDSready(fileName):
    log = open(fileName, 'r')
    WORDS = []
    WORDStoID = {}
    readUniverseOfWords(WORDS, WORDStoID)
    WORDS = frozenset(WORDS)
    return (WORDS, WORDStoID)
    #p = re.compile('^#*[a-z]+\'*[a-z]*$')
    #pNewLine = re.compile('[\r\n]+')


def classifyTweet(text, p, WORDS, WORDStoID):
    sock = createSocket()
    assert(sock != None)
    #text = re.sub(pNewLine, ' ', line)
    
    # Write out SVM features
    words = filterWords(text, p)
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

    # Send feature space representation of the tweet to SVM daemon
    #print >>sys.stderr, 'sending: "%s"' % svmString
    sock.sendall(svmString)

    score = ''    
    while True:
        data = sock.recv(16)
        #print >>sys.stderr, 'received: "%s"' % data
        score += data
        if score[-1] == '\n': # compelte string should have been received by now
            try:
                score_float = float(score)
            except ValueError:
                print "Not a numeric string."
                sock.close()
                exit(-1)
            #time.sleep(2)
            sock.close()
            return score_float    

