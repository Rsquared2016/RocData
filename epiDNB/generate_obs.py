import random
import sys

def writeDTs(numTimeSlices, numUsers):
	template1 = \
"""
%d
meeting_%d_DT_%d
%d
-1 {p0+p1} 
"""
	template2 = \
"""
%d
meeting_%d_DT_%d
%d
-1 {p0} 
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


def writeStrFile(numUsers):
	foutStr = open('dbn.str', 'w')
	template_main = \
"""\
GRAPHICAL_MODEL epiDBN

#include "dbn.header"

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
frame: 0 {

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Frame number counter used to invoke a "private" decision tree for each time slice
variable : frameNo {
 type: discrete observed 0:0 cardinality NUM_TIMESTEPS;
 switchingparents: nil;
 conditionalparents: nil using DeterministicCPT("frameNumbers");
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Health states
%s
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Twitter status updates
%s
%%%%%%%%%%%%%%%%%%%%%%%%
%% Meetings
%s
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
frame: 1 {

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Frame number counter used to invoke a "private" decision tree for each time slice
variable : frameNo {
 type: discrete observed 0:0 cardinality NUM_TIMESTEPS;
 switchingparents: nil;
 conditionalparents: nil using DeterministicCPT("frameNumbers");
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Health states evolution + impact of meetings
%s
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Twitter status updates
%s
%%%%%%%%%%%%%%%%%%%%%%%%
%% Meetings
%s
}

chunk 1:1;
"""
	
	template_pH = \
"""\
variable : H%d {
 type : discrete hidden cardinality NUM_HIDDEN_STATES;
 switchingparents: nil;
 conditionalparents: nil using DenseCPT("pH");
}
"""

	template_pT_given_H = \
"""\
variable : T%d {
 type : discrete observed %d:%d cardinality NUM_OBSERVED_STATES;
 switchingparents: nil;
 conditionalparents: H%d(0) using DenseCPT("pT_given_H");
}
"""

	template_meeting = \
"""\
variable : M%d {
 type: discrete hidden cardinality NUM_INDIVIDUALS;
 switchingparents: nil;
 conditionalparents: frameNo(0), %s using DeterministicCPT("meeting_%d");
}
"""

	template_pH_given_H_M = \
"""\
variable : H%d {
 type : discrete hidden cardinality NUM_HIDDEN_STATES;
 switchingparents: nil;
 conditionalparents: H%d(-1), M%d(-1) using DenseCPT("pH_given_H_M");
}
"""
	pH = ""
	pT_given_H = ""
	meeting = ""
	pH_given_H_M = ""
	for i in xrange(0,numUsers):
		pH += template_pH % i
		pT_given_H += template_pT_given_H % (i, i+1, i+1, i)
		parents = ""
		for j in xrange(0,numUsers):
			if j!=i:
				parents += 'H%d(0), ' % j
		# Make sure there is no comma
		parents = parents[0:-2]
		meeting += template_meeting % (i, parents, i)
		pH_given_H_M += template_pH_given_H_M % (i, i, i)
	foutStr.write(template_main % (pH, pT_given_H, meeting, pH_given_H_M, pT_given_H, meeting))
	foutStr.close()


def writeMasterFile(numUsers):
	foutMaster = open('dbn.master', 'w')
	template_main = \
"""\
#include "dbn.header"

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 			DECISION TREEs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DT_IN_FILE inline

%d %% number of decision trees

%s
%d
isMoreThan_10_DT
NUM_INDIVIDUALS_MINUS_ONE
-1 {(p0+p1)>10} %% check if sum is >10


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% DETERMINISTIC CPTs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DETERMINISTIC_CPT_IN_FILE inline

%d %% number of CPTs

%% cardinalities of parents (frameNo & health states) + cardinality of the output of the DT (0...NUM_INDIVIDUALS_MINUS_ONE)
%% TODO: bucket the number of people met

%s
%d
meeting_buckets
NUM_MEETING_NODE_PARENTS
%% cardinalities of parents (frameNo & health states) + number of buckets
NUM_TIMESTEPS %s NUM_BUCKETS 
isMoreThan_10_DT %% name of DT that implements this table
"""

	template_tree = \
"""\
%d
meeting_%d_DT
dts/meetings_%d_DT.dts

"""

	template_cpt = \
"""\
%d
meeting_%d
NUM_MEETING_NODE_PARENTS
NUM_TIMESTEPS %s NUM_INDIVIDUALS 
meeting_%d_DT

"""
	trees = ""
	cpts = ""
	for i in xrange(0,numUsers):
		trees += template_tree % (i, i, i)
		cpts += template_cpt % (i, i, 'NUM_HIDDEN_STATES ' * (numUsers-1), i)
	foutMaster.write(template_main % (numUsers+1, trees, numUsers, numUsers+1, cpts, numUsers, 'NUM_HIDDEN_STATES ' * (numUsers-1)))
	foutMaster.close()


def writeHeaderFile(numTimeSteps, numUsers):
	foutHeader = open('dbn.header', 'w')
	template = \
"""\
#ifndef COMMON_PARAMS
#define COMMON_PARAMS

%% Total number of people in the dateset
#define NUM_INDIVIDUALS %d

%% Max number of people one can meet
#define NUM_INDIVIDUALS_MINUS_ONE %d

%% Number of buckets to divide meetings into (e.g., [less than 10 meetings, 10 and more])
#define NUM_BUCKETS 3

%% 0=healthy, 1=sick
#define NUM_HIDDEN_STATES 2

%% 0=healthy tweet, 1=sick tweet, 2=no tweet
#define NUM_OBSERVED_STATES 3

%% Number of time slices (used for "private" decision trees)
#define NUM_TIMESTEPS %d

%% Number of parents of the meetings nodes (NUM_INDIVIDUALS + 1 (frameNo))
#define NUM_MEETING_NODE_PARENTS %d

#endif
"""
	foutHeader.write(template % (numUsers, numUsers-1, numTimeSteps, numUsers+1))
	foutHeader.close()


if __name__ == '__main__':
	numTimeSteps = 100
	cardinality = 3
	numUsers = 3

	# Write observations for EM here
	fout = open('data/dbn_train_%d.txt' % numTimeSteps, 'w')
	# Write true labels here
	foutLabels = open('data/dbn_train_%d_true_labels.txt' % numTimeSteps, 'w')
	# Write decision trees encoding meeting structure
	writeDTs(numTimeSteps, numUsers)
	writeStrFile(numUsers)
	writeMasterFile(numUsers)
	writeHeaderFile(numTimeSteps, numUsers)

	# Deterministic
	for t in xrange(0,numTimeSteps):
		fout.write('%d ' % t) # frameNo
		if t < numTimeSteps/3.0:
			for col in xrange(0, numUsers):
				fout.write('%d ' % 0)
				foutLabels.write('%d ' % 0)
		else:
			for col in xrange(0, numUsers):
				fout.write('%d ' % 1)
				foutLabels.write('%d ' % 1)
		fout.write('\n')
		foutLabels.write('\n')

	# # Random	
	# for t in xrange(0,numTimeSteps):
	# 	for col in xrange(0, numUsers):
	# 		fout.write('%d ' % random.randint(0, cardinality-1)),
	# 	print

	fout.close()
	foutLabels.close()
	sys.exit(0)
