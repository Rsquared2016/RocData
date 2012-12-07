# Uses results of get_colocation.py
#
# Reads input file:
# userName1
#     timeSegmentNum userName2 num_colocs@1h num_colocs_unique@1h
#     num_colocs@4h num_colocs_unique@4h
#     num_colocs@12h num_colocs_unique@12h
#     num_colocs@24h num_colocs_unique@24h
#
# into a mapping {}:
# (userName, time_segment) -> {colocated user names -> amount_of_colocation}
#
# every missing entry is 0

from customGraph import *
import cPickle as pickle
import numpy
import operator
import sys

def updateCount(dict, key, increment):
    try:
        dict[key] += increment
    except KeyError:
        dict[key] = increment

def updateCountTuple(dict, key, incrementTuple):
    try:
        dict[key] = tuple(map(operator.add, dict[key], incrementTuple))
    except KeyError:
        dict[key] = incrementTuple

def updateMap(colocMap, key, userName2, colocs):
    if not(colocMap.has_key(key)):
        colocMap[key] = {}
    colocMap[key][userName2] = colocs

def getColocs(colocMap, userName1, userName2, timeSegment):
    try:
        return colocMap[(userName1, timeSegment)][userName2]
    except KeyError:
        return (0, 0, 0, 0, 0, 0, 0, 0)
    
def readColocations():
    fin = open('nyc-colocs_0-6236', 'r')
    colocMap = {}
    for line in fin:
        splitted = line.strip().split(' ')
        (userName1, timeSegment) = tuple(splitted[0:2])
        timeSegment = int(timeSegment)
        userName2 = splitted[2]
        colocs = tuple(map(int, splitted[3:]))
        #print (userName1, timeSegment), userName2, colocs
        updateMap(colocMap, (userName1, timeSegment), userName2, colocs)
        updateMap(colocMap, (userName2, timeSegment), userName1, colocs)
    print 'Colocation map has %d entries.' % len(colocMap.items())    
    fin.close()
    pickle.dump( colocMap, open( "colocMap.pickle", "wb" ) )
    return colocMap

def updateSickColocationsCount(dict, sick, amountOfSickColocation):
    try:
        dict[amountOfSickColocation][int(sick)] += 1
    except KeyError:
        dict[amountOfSickColocation] = [0, 0]
        dict[amountOfSickColocation][int(sick)] = 1
        
#==================================================
# MAIN
#==================================================

#colocMap = readColocations()
colocMap = pickle.load(open('colocMap.pickle', "rb" ) )
print 'Colocation map has %d entries.' % len(colocMap.items()) 
print colocMap[colocMap.keys()[0]]

# Consider causality between this many segments (i.e. days) apart
OFFSET = int(sys.argv[2])

G = customGraph('ALL.dot_undirected.dot')
allUsers = G.getNodeNameSet()
#G.removeSmallCliques(4)

allSickUsers = set()
pickleFile = sys.argv[1]
segmentToSick = pickle.load(open(pickleFile, "rb" ) )

prior = 0
for (i,s) in enumerate(segmentToSick.values()):
    print 'Segment %d: %d sick users' % (i, len(s))
    #print '%d' % len(s)
    allSickUsers.update(s)
    prior += len(s)/float(len(allUsers))
prior = prior/len(segmentToSick.keys())
print 'Prior P(sick) = %.4f' % prior
fprior = open('%s_prior' % pickleFile, 'w')
fprior.write(str(prior)+'\n')
fprior.close()

numSlicesPerSequence = len(segmentToSick.keys()) + 1 # 0 divides sequences
numSequences = len(allUsers)
numFeaturesPerSlice = (OFFSET+1)*3 + 1

#The observation matrix: rows are sequences of people's health status; cols are features for each (person x slice) combination
# slice1: person1_feature1 person1_feature2 ...
# slice2: person1_feature1 person1_feature2 ...
# ...
# sliceN:   person4_feature1 person4_feature2 ...
# sliceN+1: person5_feature1 person5_feature2 ...
#
# Current features:
# 1. Weekday (1=Mon ... 7=Sun)
# 2. Amount of co-location with sick individuals in slice-OFFSET day
# 3. Amount of co-location with sick individuals in slice-OFFSET+1 day
# 4. Amount of co-location with sick individuals in slice-OFFSET+2 day
# 5. Amount of co-location with sick individuals in slice-OFFSET+3 day
# ...
# n. Amount of co-location with sick individuals in slice day
# n+1. Number of unique sick individuals encoutnered in slice-OFFSET day
# n+2. Number of unique sick individuals encoutnered in slice-OFFSET+1 day
# n+3. Number of unique sick individuals encoutnered in slice-OFFSET+2 day
# n+4. Number of unique sick individuals encoutnered in slice-OFFSET+3 day
# ...
# m.   Number of unique sick individuals encoutnered in slice day
# m+1. Number of sick friends in the slice-OFFSET day
# m+2. Number of sick friends in the slice-OFFSET+1 day
# m+3. Number of sick friends in the slice-OFFSET+2 day
# ...
# k.   Number of sick friends in the slice day

#X = numpy.zeros((numSequences*numSlicesPerSequence, numFeaturesPerSlice), dtype=int)

# The label vector: health state for each (person x slice) combination
# 1=healthy
# 2=sick
#y = numpy.zeros((numSequences*numSlicesPerSequence, 1), dtype=int)

# name -> (num_colocs@1h num_colocs_unique@1h
#     num_colocs@4h num_colocs_unique@4h
#     num_colocs@12h num_colocs_unique@12h
#     num_colocs@24h num_colocs_unique@24h num_unique_sick_individuals_encountered) added up over the entire dataset
userNameToSickEncounters = {}

# name -> num of friend-sick days over the entire dataset
# (1 friend sick for 3 days and 2 friends sick for 1 day each = 5 friend-sick days)
userNameToSickFriends = {}

colocType = 4
MEMORY = 4
for (sequence,A) in enumerate(allUsers):
    #if sequence > 2:
    #    break
    alreadySick = set()
    friends = G.getFriends(A)
    for slice in xrange(0,len(segmentToSick.keys())):
        rowIdx = sequence*numSlicesPerSequence + slice
        #sickSlice = segmentToSick[slice]

        # A is assumed sick in the slice where he declares it + in MEMORY following slices
        sickSliceMemory = segmentToSick[slice]
        for day in xrange(max(0,slice-MEMORY), slice):
            sickSliceMemory.update(segmentToSick[day])
            
        #X[rowIdx][0] = (slice + 2)%7 + 1 # data starts on Wednesday May 19th
        # Determine label for user A in this slice. Healty=1 Sick=2
        #y[rowIdx] = int(A in sickSliceMemory) + 1
        for previous in xrange(max(0,slice-OFFSET), slice+1):
            #featureNum = (slice-previous)*OFFSET
            #print slice, previous#, featureNum
           
            # Update sick set
            sickPrevious = segmentToSick[previous]
            for day in xrange(max(0,previous-MEMORY), previous):
                sickPrevious.update(segmentToSick[day])
            
            # Determine observed feature values

            # Count sick friends    
            numSickFriends = len(friends.intersection(sickPrevious))
            updateCount(userNameToSickFriends, A, numSickFriends)

            # Cound co-locations
            colocA = (0, 0, 0, 0, 0, 0, 0, 0)
            encountered = 0 # encountered people count
            for B in sickPrevious:
                colocAB = getColocs(colocMap, A, B, previous)
                colocA = tuple(map(operator.add, colocA, colocAB))
                if colocAB[colocType] > 0:
                    encountered += 1

            updateCountTuple(userNameToSickEncounters, A, colocA + (encountered,)) # extend tuple
                    
            #X[rowIdx][1+(slice-previous)] = colocA + 1       
            #X[rowIdx][1+(slice-previous)+(OFFSET+1)] = encountered + 1
            #X[rowIdx][1+(slice-previous)+2*(OFFSET+1)] = numSickFriends + 1
            #print 1+(slice-previous), 1+(slice-previous)+OFFSET+1, 1+(slice-previous)+(1+OFFSET)*2
    if (sequence%100 == 0):
        print '%2.1f%% done' % (100*sequence/float(len(allUsers)))


# Pickle mapping for health WSDM paper
pickle.dump(userNameToSickFriends, open('userNameToSickFriends.pickle', 'wb') )
pickle.dump(userNameToSickEncounters, open('userNameToSickEncounters.pickle', 'wb') )

# Write matrices out
#fX = open('X_%s_coloc-%d_offset-%d_memory-%d.txt' % (pickleFile[:-7], colocType, OFFSET, MEMORY), 'w')
#for row in X:
#    for c in row:
#        fX.write('%d ' % c)
#    fX.write('\n')
#fX.close()

#fy = open('y_%s_coloc-%d_offset-%d_memory-%d.txt' % (pickleFile[:-7], colocType, OFFSET, MEMORY), 'w')
#for row in y:
#    fy.write('%d\n' % row)
#fy.close()


       
