"""
This script replicates databases from one CouchDB server to an other.

This is mainly for backup purposes or "priming" a new server before
setting up trigger based replication. But you can also use the
'--continuous' option to set up automatic replication on newer
CouchDB versions.

Use 'python replicate.py --help' to get more detailed usage instructions.

Example:
python replicate.py http://166.78.236.179:5984 http://dev.166.78.236.179:5984 --continuous

"""

import couchdb.client
import optparse
import sys
import time

def getActiveReplications(server):
    tasks = server.tasks()
    active_reps = []
    for r in [task for task in tasks if task['type']=='replication']:
        print r['target']
        target = r['target'].split('/')[-2]
        source = r['source'].split('/')[-2]
        assert(target==source)
        active_reps.append(source)
    return active_reps

def main():
    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--database',
        action='append',
        dest='dbnames',
        help='Database to replicate. Can be given more than once. [all databases]')
    parser.add_option('--continuous',
        action='store_true',
        dest='continuous',
        help='trigger continuous replication in cochdb')
    parser.add_option('--compact',
        action='store_true',
        dest='compact',
        help='compact target database after replication')

    options, args = parser.parse_args()
    if len(args) != 2:
        raise parser.error('need source and target arguments')

    src, tgt = args
    if not src.endswith('/'):
        src += '/'
    if not tgt.endswith('/'):
        tgt += '/'

    source_server = couchdb.client.Server(src)
    source_server.resource.credentials = ('admin', 'admin')
    active_replications = [] #getActiveReplications(source_server)
    target_server = couchdb.client.Server(tgt)
    target_server.resource.credentials = ('admin', 'admin')

    if not options.dbnames:
        dbnames = sorted(i for i in source_server)
    else:
        dbnames = options.dbnames

    for dbname in sorted(dbnames, reverse=True):
        sdb = '%s%s' % (src, dbname)
        if dbname[0] == '_' or dbname in active_replications:
            print '"%s" is already replicating or is a _* db' % dbname
            #source_server.replicate(sdb, dbname, continuous=options.continuous, cancel=True)
            continue
        print 'Replicating db %s' % dbname
        target_server.replicate(sdb, dbname, continuous=options.continuous, create_target=True)

    if not options.compact:
        return

    sys.stdout.flush()
    for dbname in dbnames:
        if dbname[0] == '_':
            continue
        target_server[dbname].compact()

if __name__ == '__main__':
    main()
