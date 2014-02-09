import sys
import re

f_tokens = open(sys.argv[1], 'r')
tokens = []
p = re.compile(' ')

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
            print "Skipping weight"
            continue
        weightToToken[float(w)] = tokens[int(num)-1]
        weights += 1

N = 10
for (w, token) in sorted(weightToToken.items(), reverse=True)[0:N]:
    print '%s %.4f' % (token, w)

print "------------------------------------------------------------"
    
for (w, token) in sorted(weightToToken.items(), reverse=False)[0:N]:
    print '%s %.4f' % (token, w)

print "------------------------------------------------------------"
#print "Multi-word-features:"
#for (w, token) in sorted(weightToToken.items(), reverse=True):
#    if p.search(token) != None:
#        print '%s %.4f' % (token, w)

print '%d weights found' % weights
