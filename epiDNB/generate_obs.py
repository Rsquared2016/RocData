import random

def writeDTs(numTimeSlices, numUsers):
	template1 = \
"""
%d
meeting_%d_DT_%d
%d
-1 {(p0+p1)} 
"""
	template2 = \
"""
%d
meeting_%d_DT_%d
%d
-1 {(p0)} 
"""
	for user in xrange(0,numUsers):
		foutDT = open('dts/meetings_%d_DT.dts' % user, 'w')
		foutDT.write('%d %% number of decision trees in this file\n\n' % numTimeSlices)
		foutDT.write('% These decision trees return the sum of select parents that represent encountered people (=the estimated number of distinct sick people met)\n')
		for dtNum in xrange(0,numTimeSlices):
			if random.randint(0, 1) == 0:
				foutDT.write(template1 % (dtNum, user, dtNum, numUsers-1))
			else:
				foutDT.write(template2 % (dtNum, user, dtNum, numUsers-1))
		foutDT.close()


if __name__ == '__main__':
	numLines = 100
	cardinality = 3
	numColumns = 3

	# Write observations for EM here
	fout = open('data/dbn_train_%d.txt' % numLines, 'w')
	# Write true labels here
	foutLabels = open('data/dbn_train_%d_true_labels.txt' % numLines, 'w')
	# Write decision trees encoding meeting structure
	writeDTs(numLines, numColumns)

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
