# Load SVM model and classify tweets interactivelly
# example: python classify.py words.txt svm

import sys
import re
import readline
from extract_features import *

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode emacs')

WORDSfile = sys.argv[1]
SVMfile = sys.argv[2]

WORDStoID = readUniverseOfWords(WORDSfile)
model = loadSVM(SVMfile)
p = re.compile('^#*[a-z]+\'*[a-z]*$')

while True:
    line = raw_input('Text to classify: ')
    print 'HEALTH CLASSIFICATION: %f' % classifyTweetPython(line.strip(), p, WORDStoID, model)
