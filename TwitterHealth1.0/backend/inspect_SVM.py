# Shows most significant features in the SVM model
# example: python inspect_SVM.py words.txt svm

import sys
import re

f_tokens = open(sys.argv[1], 'r')
tokens = []

for line in f_tokens:
    tokens.append(line.strip())

weightToToken = {}
f_model = open(sys.argv[2], 'r')
weights = 0
for line in f_model:
    # skip first lines
    if len(line) < 1000:
        continue
    featureWeights = line.strip().split(' ')
    for f in featureWeights:
        try:
            (num, w) = f.split(':')
        except ValueError:
            continue
        weightToToken[float(w)] = tokens[int(num)-1]
        weights += 1

N = None#100
for (w, token) in sorted(weightToToken.items(), reverse=True)[0:N]:
    print '%s %.10f' % (token, w)

print "------------------------------------------------------------"
    
for (w, token) in sorted(weightToToken.items(), reverse=False)[0:N]:
    print '%s %.10f' % (token, w)

print "------------------------------------------------------------"
print '%d weights found' % weights
