clean:
	rm -f *.dat *.meta *.log

huge: clean
	#./couchdb_bulk_perf.py 10 4000000 1 | tee huge-10-4000000.log
	#./couchdb_bulk_perf.py 100 4000000 1 | tee huge-100-4000000.log
	./couchdb_bulk_perf.py 1000 4000000 1
	#./couchdb_bulk_perf.py 10000 4000000 1 | tee huge-10000-4000000.log
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
