# Show the latent effect of friendship by showing contagion via friends who have NOT been recently co-located
# python -OO contagion_friendship-colocation.py segmentToSick_0.8-good.pickle 1

from customGraph import *
import pickle
import sys

def updateSickFriendCount(dict, sick, numSickFriends):
    try:
        dict[numSickFriends][int(sick)] += 1
    except KeyError:
        dict[numSickFriends] = [0, 0]
        dict[numSickFriends][int(sick)] = 1
        
def getProbSickGivenFriendlistSize():
    '''Get prior cond. prob Pr(prob ob being sick | # of friends (any))'''
    sickFriendCountToHealthState = {}
    for (i,s) in enumerate(segmentToSick.values()):
        u = s.intersection(allUsers)
        for A in allUsers:
            numFriends = len(G.getFriends(A))
            updateSickFriendCount(sickFriendCountToHealthState, (A in u), numFriends)

    fout = open('sickFriendCountToHealthState.txt', 'w')
    for (numSickFriends, stats) in sickFriendCountToHealthState.items():
        if stats[1] == 0:
            continue
        print '%d %d %d %.4f' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1]))
        fout.write('%d %d %d %.4f\n' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1])))
    fout.close()
    exit()

def updateMap(colocMap, key, userName2, colocs):
    if not(colocMap.has_key(key)):
        colocMap[key] = {}
    colocMap[key][userName2] = colocs

def getColocs(colocMap, userName1, userName2, timeSegment):
    try:
        return colocMap[(userName1, timeSegment)][userName2]
    except KeyError:
        return (0, 0, 0, 0, 0, 0)
    
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
    return colocMap


#==================================================
# MAIN
#==================================================

colocMap = readColocations()

# Consider causality between this many segments (i.e. days) apart
OFFSET = int(sys.argv[2])

G = customGraph('ALL.dot_undirected.dot')
allUsers = G.getNodeNameSet()

allSickUsers = set()
pickleFile = sys.argv[1]
segmentToSick = pickle.load(open(pickleFile, "rb" ) )

prior = 0
for (i,s) in enumerate(segmentToSick.values()):
    #print 'Segment %d: %d sick users' % (i, len(s))
    #print '%d' % len(s)
    allSickUsers.update(s)
    prior += len(s.intersection(allUsers))/float(len(allUsers))
alwaysHealthy = allUsers.difference(allSickUsers)
prior = prior/len(segmentToSick.keys())
print 'Prior P(sick) = %.4f' % prior
fprior = open('prior_friendship-colocation.txt', 'w')
fprior.write(str(prior)+'\n')
fprior.close()
print('# allSick / # all users = %f' % (float(len(allSickUsers.intersection(allUsers)))/len(allUsers)))

#getProbSickGivenFriendlistSize()

# Get a relationship between the # of A's sick friends @ t-OFFSET and the probability that A is sick @ t
sickFriendCountToHealthState = {}
alreadySick = set()
MEMORY = 6
colocType = 2
numFriendsEncountered = 0
for i in range(OFFSET,len(segmentToSick.keys())):
    sickT = segmentToSick[i].intersection(allUsers)
    sickTminus1 = segmentToSick[i-OFFSET].intersection(allUsers)
    healthyT = allUsers.difference(sickT)
    healthyTminus1 = allUsers.difference(sickTminus1)
    if i>=MEMORY:
        sickWeekAgo = segmentToSick[i-MEMORY]
        alreadySick = alreadySick.difference(sickWeekAgo)
    alreadySick.update(sickTminus1)
    for A in allUsers:
        friends = G.getFriends(A)
        sickFriends = set()
        for B in friends:
            colocAB = getColocs(colocMap, A, B, i-OFFSET)[colocType]
            # eliminate all co-located friends
            if colocAB <= 0:
                sickFriends.add(B)
            else:
                #Friend encountered
                numFriendsEncountered += 1
        sickFriends = sickFriends.intersection(alreadySick)
        updateSickFriendCount(sickFriendCountToHealthState, (A in sickT), len(sickFriends))
print 'Total number of friend encounters = %d' % numFriendsEncountered
print 'Average number of friend encounters = %f' % (float(numFriendsEncountered)/len(allUsers)/(len(segmentToSick.keys())-OFFSET))
    
fout = open('sickNonColocatedFriendCountToHealthState.txt', 'w')
for (numSickFriends, stats) in sickFriendCountToHealthState.items():
    if stats[1] == 0:
        continue
    print '%d %d %d %.4f' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1]))
    fout.write('%d %d %d %.4f\n' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1])))
fout.close()
