import random

numLines = 100
cardinality = 3
numColumns = 3

# Write observations for EM
fout = open('dbn_train_%s.txt' % numLines, 'w')
# Write true labels
foutLabels = open('dbn_train_%s_true_labels.txt' % numLines, 'w')

# Deterministic
for lineNum in xrange(0,numLines):
	if lineNum < numLines/3.0:
		for col in xrange(0, numColumns):
			fout.write('%d ' % 0)
			foutLabels.write('%d\n' % 0)
	else:
		for col in xrange(0, numColumns):
			fout.write('%d ' % 1)
			foutLabels.write('%d\n' % 1)
	fout.write('\n')

# # Random	
# for lineNum in xrange(0,numLines):
# 	for col in xrange(0, numColumns):
# 		fout.write('%d ' % random.randint(0, cardinality-1)),
# 	print

fout.close()
foutLabels.close()
