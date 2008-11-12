set term png small
set out 'results.png'
plot 'bulk-perf-10-100000.dat' with lines, \
     'bulk-perf-100-100000.dat' with lines, \
     'bulk-perf-1000-100000.dat' with lines
