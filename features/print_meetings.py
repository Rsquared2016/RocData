"""
	Takes a meetings data structure and prints it out.

    print_meetings.py <pickle-file-path>

    example:
        python print_meetings.py meetings_toy.pickle
"""

import cPickle as pickle
import sys

meetings = pickle.load(open(sys.argv[1], 'rb'))

for day in sorted(meetings):
	print '%s:' % day
	for (p1, p2s) in sorted(meetings[day].items()):
		print '\t%s <-> %s...' % (p1, str(p2s)[0:80])