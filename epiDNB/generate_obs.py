import random

numLines = 100
cardinality = 3
numColumns = 3

# Write observations for EM here
fout = open('data/dbn_train_%d.txt' % numLines, 'w')
# Write true labels here
foutLabels = open('data/dbn_train_%d_true_labels.txt' % numLines, 'w')

# Deterministic
for lineNum in xrange(0,numLines):
	if lineNum < numLines/3.0:
		for col in xrange(0, numColumns):
			fout.write('%d ' % 0)
			foutLabels.write('%d ' % 0)
	else:
		for col in xrange(0, numColumns):
			fout.write('%d ' % 1)
			foutLabels.write('%d ' % 1)
	fout.write('\n')
	foutLabels.write('\n')

# # Random	
# for lineNum in xrange(0,numLines):
# 	for col in xrange(0, numColumns):
# 		fout.write('%d ' % random.randint(0, cardinality-1)),
# 	print

fout.close()
foutLabels.close()
