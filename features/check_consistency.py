"""
    Ensures logical consistency of meetings file.

    check_consistency.py <pickle-file-path> <inconsistencies-dump>

    example:
        python check_consistency.py meetings_toy.pickle check_consistency.dump
"""

import cPickle as pickle
#from datetime import datetime
import pprint
import sys

meetings = pickle.load(open(sys.argv[1], 'rb'))
ifilename = sys.argv[2]
inconsistencies = { 'asymmetric': [], 'duplicate': [] }

for (date, user_meetings) in meetings.items():
    #print "Checking time slice %s ..." % date.strftime("%Y-%m-%d")
    for (user, encounters) in user_meetings.items():
        #print "\tChecking user %s ..." % user
        for encounter in encounters:
            if user == encounter:
                print "\t\t\tERROR: %s -> %s is not possible!" % (user, encounter)
                inconsistencies['duplicate'].append((encounter, user))
                continue
            #print "\t\tChecking %s -> %s ..." % (user, encounter)
            if (encounter not in meetings[date]) or (user not in meetings[date][encounter]):
                print "\t\t\tERROR: %s -> %s is not present!" % (encounter, user)
                inconsistencies['asymmetric'].append((encounter, user))
            #else:
            #    print "\t\t\t%s -> %s found, continuing..." % (encounter, user)

final_number = len(inconsistencies['duplicate']) + len(inconsistencies['asymmetric'])
print "Final # of inconsistencies: %d" % final_number
if final_number > 0:
    with open(ifilename, 'w+') as ifile:
        pp = pprint.PrettyPrinter(indent = 4, stream = ifile)
        pp.pprint(inconsistencies)
    exit(-1)