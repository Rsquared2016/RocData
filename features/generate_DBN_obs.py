"""
	Takes tweeting calendar and meetings data structures and outputs observation file for DBN model.

	generate_DBN_obs.py <tweeting-pickle-file-path> <meeting-pickle-file-path>

	example:
		python generate_DBN_obs.py health_toy.pickle meetings_toy.pickle
"""

import cPickle as pickle
import sys

def writeDTs(usersList, meetings, numTimeSteps, numUsers, twitterIdtoDBNid):
	template = \
"""
0
meeting_%d_DT
%d
0 %d %s default %% query on parent 0 (frameNo), make %d splits
%s
 -1 -1
"""
	for user in usersList:
		foutDT = open('../epiDBN/dts/meetings_%d_DT.dts' % twitterIdtoDBNid[user], 'w+')
		foutDT.write('1 %% number of decision trees in this file\n\n')
		foutDT.write('%% Conditioned on a given time step, this decision tree returns the sum of select parents that represent encountered people (=the estimated number of distinct sick people met)\n')
		
		# Generate all possible time slice values (0 ... NUM_TIMESTEPS-1)
		splits = ''
		for i in xrange(0, numTimeSteps):
			splits += '%d ' % i
		
		leaves = ''
		for (t, (_, dic)) in enumerate(sorted(meetings.items())):
			leaves += ' -1 '
			try:
				usersMet = dic[user]							
				# There is at least one person who met $user	
				usersMetTransformed = [twitterIdtoDBNid[u] for u in usersMet]
				leaves += '{'
				for userMet in usersMetTransformed:
					leaves += 'p%d+' % userMet
				leaves = leaves[0:-1] # remove last +
				leaves += '}\n'
			except KeyError: # No met users
				leaves += '0\n'
				continue
		foutDT.write(template % (twitterIdtoDBNid[user], numUsers, numTimeSteps+1, splits, numTimeSteps+1, leaves))
		foutDT.close()


def writeStrFile(numUsers):
	foutStr = open('../epiDBN/dbn.str', 'w')
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
 conditionalparents: nil using DenseCPT("frameNumbers"); %% This CPT is left undefined which makes it uniform when -allocateDenseCpts 2
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
 conditionalparents: nil using DenseCPT("frameNumbers"); %% This CPT is left undefined which makes it uniform when -allocateDenseCpts 2
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
	foutMaster = open('../epiDBN/dbn.master', 'w')
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
NUM_MEETING_NODE_PARENTS
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
	foutHeader = open('../epiDBN/dbn.header', 'w')
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
	foutHeader.write(template % (numUsers, numUsers-1, numTimeSteps, numUsers))
	foutHeader.close()

def writeHealthObs(usersList, health, numTimeSteps):
	""" Dump observations to specified file """

	# Write observations for EM here
	fout = open('../epiDBN/data/dbn_train_%d.txt' % numTimeSteps, 'w+')

	# Write true labels here
	#foutLabels = open('../epiDBN/data/dbn_train_%d_true_labels.txt' % numTimeSteps, 'w')

	# Header
	fout.write('%% TIME_STEP ')
	for (newID, origID) in enumerate(usersList):
		fout.write('%d(%s) ' % (newID, origID))
	fout.write('\n')

	# Observations: TIME_STEP + user health states (1=user tweeted something sick on a given day, 0=all his tweets were healthy during the day, 2=no tweet)
	for (t, (_, dic)) in enumerate(sorted(health.items())):
		fout.write('%d ' % t) # Write time index as the first observation on each line
		for user in usersList:
			fout.write('%d ' % dic[user])
		fout.write('\n')
	fout.close()




########################################################################################################################
# MAIN

health = pickle.load(open(sys.argv[1], 'rb'))   # { datetime: { userID: health(0-2) }, ... }
meetings = pickle.load(open(sys.argv[2], 'rb')) # { datetime: { userID: [userIDmet1, userIDmet2], ... }, ... }

# Extract user set
users = set()
# for dic in meetings.values():
# 	for (key, value) in dic.items():
# 		users.add(key)
# 		users.update(value)
for dic in health.values():
	users.update(dic.keys())
print 'Found %d users.' % len(users)

# Organized users
usersList = sorted(list(users))
numUsers = len(usersList)
numTimeSteps = len(health.keys())
assert(numTimeSteps==len(meetings.keys()))

# Induce mapping twitterID -> DBNuserID (0 ... NUM_USERS-1)
twitterIdtoDBNid = {}
for (newID, origID) in enumerate(usersList):
	twitterIdtoDBNid[origID] = newID
assert(len(twitterIdtoDBNid.keys()) == numUsers)

# Write decision trees encoding meeting structure
writeHealthObs(usersList, health, numTimeSteps)
writeDTs(usersList, meetings, numTimeSteps, numUsers, twitterIdtoDBNid)
writeStrFile(numUsers)
writeMasterFile(numUsers)
writeHeaderFile(numTimeSteps, numUsers)

