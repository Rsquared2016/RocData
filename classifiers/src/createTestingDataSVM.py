# Example: 
#  python -OO createTestingDataSVM.py ../nyc.trim.sort svm_model/training_data.words

import os
import sys
from extract_features import *
from tweetReader import *

testFile  = sys.argv[1]
wordsFile = sys.argv[2]

filePrefix = os.path.splitext(os.path.basename(sys.argv[2]))[0]
filePath   = sys.argv[2][ 0 : - (len(filePrefix ) + 6) ]

output = open('%s/testing_data.dat' % filePath, 'w+')

WORDStoID = readUniverseOfWords(wordsFile)
WORDS = set(WORDStoID.keys())

reader = tweetReader(testFile) 
while True:
	ret = reader.getNextTweet()
	if ret == None:
		break
	elif ret == 'Err':
		continue
	(tweet, _) = ret
	output.write(tweetToSVMformat(tweet.text, WORDS, WORDStoID))
	
