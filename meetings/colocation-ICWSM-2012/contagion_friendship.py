
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
    
# Consider causality between this many segments (i.e. days) apart
OFFSET = int(sys.argv[2])

G = customGraph('ALL.dot_undirected.dot')
allUsers = G.getNodeNameSet()
#G.removeSmallCliques(4)

allSickUsers = set()
pickleFile = sys.argv[1]
segmentToSick = pickle.load(open(pickleFile, "rb" ) )

#segmentToSick = pickle.load(open( "segmentToSick-1.1.pickle", "rb" ) )
#segmentToSick = pickle.load(open( "segmentToSick-0.8-sick.pickle", "rb" ) )
#segmentToSick = pickle.load(open( "segmentToSick-1.1-new.pickle", "rb" ) )
#segmentToSick = pickle.load(open( "segmentToSick-0.93.pickle", "rb" ) ) # nice
#segmentToSick = pickle.load(open( "segmentToSick-0.8.pickle", "rb" ) ) # nice
#segmentToSick = pickle.load(open( "segmentToSick-0.9-new.pickle", "rb" ) )

prior = 0
for (i,s) in enumerate(segmentToSick.values()):
    #print 'Segment %d: %d sick users' % (i, len(s))
    #print '%d' % len(s)
    allSickUsers.update(s)
    prior += len(s.intersection(allUsers))/float(len(allUsers))
alwaysHealthy = allUsers.difference(allSickUsers)
prior = prior/len(segmentToSick.keys())
print 'Prior P(sick) = %.4f' % prior
fprior = open('prior-frienship.txt', 'w')
fprior.write(str(prior)+'\n')
fprior.close()
print('# allSick / # all users = %f' % (float(len(allSickUsers.intersection(allUsers)))/len(allUsers)))

#getProbSickGivenFriendlistSize()

# Get a relationship between the # of A's sick friends @ t-OFFSET and the probability that A is sick @ t
sickFriendCountToHealthState = {}
alreadySick = set()
MEMORY = 4
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
        #sickFriends = friends.intersection(sickTminus1)
        sickFriends = friends.intersection(alreadySick)
        #healthyFriends = friends.intersection(alwaysHealthy)
        #healthyFriends = friends.intersection(healthyTminus1)
        updateSickFriendCount(sickFriendCountToHealthState, (A in sickT), len(sickFriends))
        #updateSickFriendCount(sickFriendCountToHealthState, (A in sickT), len(healthyFriends))
        #updateSickFriendCount(sickFriendCountToHealthState, (A in sickT), len(friends))
        #if friends<=healthyFriends:
        #    updateSickFriendCount(sickFriendCountToHealthState, (A in sickT), len(friends))

fout = open('sickFriendCountToHealthState-0.8-final-nice.txt', 'w')
for (numSickFriends, stats) in sickFriendCountToHealthState.items():
    if stats[1] == 0:
        continue
    print '%d %d %d %.4f' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1]))
    fout.write('%d %d %d %.4f\n' % (numSickFriends, stats[0], stats[1], float(stats[1])/(stats[0]+stats[1])))
fout.close()
exit()



# Calculate probability P(A is sick at t | at least one of A's friends (B) is sick at t-OFFSET)
yes = 0
no = 0
for i in range(OFFSET,len(segmentToSick.keys())):
    sickT = segmentToSick[i].intersection(allUsers)
    sickTminus1 = segmentToSick[i-OFFSET].intersection(allUsers)
    healthyT = allUsers.difference(sickT)
    healthyTminus1 = allUsers.difference(sickTminus1)
    for A in sickT:
        # A is sick and at least one of his friends exhibited sickness in the previous time step
        if G.getFriends(A).intersection(sickTminus1) != None:
            yes += 1
        # A is sick but all his friends are healthy in the previous time step
        # if G.getFriends(A).intersection(healthyTminus1) == None:
        if len(G.getFriends(A).intersection(healthyTminus1)) < numFriends:
            no += 1

    


print 'Yes: %d' % yes
print 'No:  %d' % no
print 'P(A sick at t | at least one of A\'s friends (B) is sick at t-%d) = %.4f' % (OFFSET, float(yes)/(yes+no))                 

