#!/usr/bin/env python

import Queue
from threading import Lock, Thread, Event
from sys import maxint, argv, exit
from time import time, sleep
from random import randint, choice
from couchdb import Server


def gen_document():
    return dict(name   = randint(0, maxint),
                color  = choice(['reg', 'green', 'blue', 'yellow', 'pink', 'orange', 'gray', 'black', 'white']),
                type   = choice(['machine', 'chemicals', 'human', 'building', 'animal']),
                tstamp = randint(0, maxint))


count = 0
timer = 0
internal_counter = 0

def main(bulk_size, up_to, num_threads):
    global timer
    s = Server('http://localhost:5984')
    if 'test' in s:
        del s['test']
    db = s.create('test')

    stats_file = 'bulk-perf-%s-%s-%s.dat' % (bulk_size, up_to, num_threads)
    title_file = stats_file + '.meta'
    f = open(title_file, 'w')
    f.write('Bulk size: %s, num threads: %s' % (bulk_size, num_threads))
    f.close()

    stats_file = open(stats_file, 'w')

    stats_lock = Lock()
    exit_event = Event()

    chunks = Queue.Queue()

    def process_chunks():
        global count, timer, internal_counter

        s = Server('http://localhost:5984')
        db = s['test']

        while not exit_event.isSet():
            try:
                chunk = list(chunks.get(timeout=5))
                chunks.task_done()

                db.update(chunk)

                stats_lock.acquire()
                try:
                    count += bulk_size
                    internal_counter += bulk_size

                    if internal_counter >= max(num_threads*bulk_size, up_to/1000):
                        end = time()

                        stats_file.write('%s %s\n' % (count, internal_counter/float(end-timer)))
                        stats_file.flush()

                        timer = end
                        internal_counter = 0
                        print '%.1f%%' % (float(count) / up_to * 100)
                finally:
                    stats_lock.release()

            except Queue.Empty:
                pass

            except Exception, e:
                print 'Exception: %r' % (e,)
                chunks.put(chunk)
                sleep(1)

    def data_generator():
        for chunk_num in xrange(up_to / bulk_size):
            while chunks.qsize() > 100:
                sleep(0.5)
            chunks.put((gen_document() for i in xrange(bulk_size)))

        print 'Data generation done, waiting for workers.'
        chunks.join()
        print 'Signaling to exit.'
        exit_event.set()

    def loop():
        threads = [Thread(target = process_chunks) for i in xrange(num_threads)]
        threads.append(Thread(target = data_generator))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    try:
        timer = time()
        loop()
    except Exception, e:
        print 'Exception caught: %r' % e


    stats_file.close()

if __name__ == '__main__':
    if len(argv) != 4:
        print 'Usage: %s <bulk_size> <doc_count> <num_threads>' % argv[0]
        exit(1)

    main(int(argv[1]), int(argv[2]), int(argv[3]))
