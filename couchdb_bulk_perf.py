#!/usr/bin/env python

from sys import maxint, argv, exit
from time import time
from random import randint, choice
from couchdb import Server


def gen_document():
    return dict(name   = randint(0, maxint),
                color  = choice(['reg', 'green', 'blue', 'yellow', 'pink', 'orange', 'gray', 'black', 'white']),
                type   = choice(['machine', 'chemicals', 'human', 'building', 'animal']),
                tstamp = randint(0, maxint))


def main(bulk_size, up_to):
    s = Server('http://localhost:5984')
    if 'test' in s:
        del s['test']
    db = s.create('test')

    stats_file = 'bulk-perf-%s-%s.dat' % (bulk_size, up_to)
    stats = []

    def loop():
        count = 0
        while count < up_to:
            docs = (gen_document() for i in xrange(bulk_size))

            start = time()
            db.update(docs)
            end = time()

            count += bulk_size
            stats.append((count, bulk_size/float(end-start)))
            print '%.1f%%' % (float(count) / up_to * 100)


    try:
        loop()
    except Exception, e:
        print 'Exception caught: %r' % e


    print 'Writing stats to the %r' % stats_file
    f = open(stats_file, 'w')
    try:
        for stat in stats:
            f.write('%s %s\n' % stat)
    finally:
        f.close()

if __name__ == '__main__':
    if len(argv) != 3:
        print 'Usage: %s <bulk_size> <doc_count>' % argv[0]
        exit(1)

    main(int(argv[1]), int(argv[2]))
