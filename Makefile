clean:
	rm -f *.dat *.meta

huge: clean
	./couchdb_bulk_perf.py 10 10000000 1
	./couchdb_bulk_perf.py 100 10000000 1
	./couchdb_bulk_perf.py 1000 10000000 1
	./couchdb_bulk_perf.py 10000 10000000 1
	./gen_plot.sh huge.png

bulk_size: clean
	./couchdb_bulk_perf.py 10 100000 1
	./couchdb_bulk_perf.py 100 100000 1
	./couchdb_bulk_perf.py 1000 100000 1
	./couchdb_bulk_perf.py 10000 100000 1
	./gen_plot.sh bulk-size.png

threads: clean
	./couchdb_bulk_perf.py 100 100000 1
	./couchdb_bulk_perf.py 100 100000 2
	./couchdb_bulk_perf.py 100 100000 4
	./couchdb_bulk_perf.py 100 100000 8
	./couchdb_bulk_perf.py 100 100000 16
	./gen_plot.sh threads.png
