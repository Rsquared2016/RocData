# Example: 
#  python -OO createTestingDataSVM.py ../nyc.trim.sort svm_model/training_data.words

import sys
from extract_features import *
from tweetReader import *

testFile = sys.argv[1]
wordsFile  = sys.argv[2]

output = open('svm_model/testing_data.dat', 'w+')

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
	
