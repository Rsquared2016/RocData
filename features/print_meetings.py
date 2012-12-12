"""
	Takes a meetings data structure and prints it out.

    print_meetings.py <pickle-file-path> [pretty]

    example:
        python print_meetings.py meetings_toy.pickle
"""

import cPickle as pickle
import pprint
import sys

meetings = pickle.load(open(sys.argv[1], 'rb'))
print_pretty = sys.argv[2] and sys.argv[2] == "pretty"

if not print_pretty:
    for day in sorted(meetings):
    	print '%s:' % day
    	for (p1, p2s) in sorted(meetings[day].items()):
    		print '\t%s <-> %s...' % (p1, str(p2s)[0:80])
else:
    pp = pprint.PrettyPrinter(indent = 4, stream = sys.stdout)
    pp.pprint(meetings)