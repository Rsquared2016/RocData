"""
    meetings.py <file-path> [<distance-slack> <time-slack>]
"""

import couchdb
import json
from datetime import datetime, timedelta
import sys

""" grab cmdline args and initialize parameters """
distance_slack = float(sys.argv[2]) if len(sys.argv) >= 2 else 0.1
time_slack = float(sys.argv[3]) if len(sys.argv) >= 3 else 1

