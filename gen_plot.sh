#!/bin/bash

OUTPUT_FILE="$1"
PLOT_FILE="temp.plt"

echo "set term png small" > $PLOT_FILE
echo "set out '$OUTPUT_FILE'" >> $PLOT_FILE
echo "plot \\" >> $PLOT_FILE

for FILE in *.dat; do
    echo -n "'$FILE' title '`cat $FILE.meta`' with lines" >> $PLOT_FILE
    if [ $FILE != `ls *.dat | tail -1` ]; then
        echo ", \\" >> $PLOT_FILE
    fi
done

gnuplot $PLOT_FILE

rm $PLOT_FILE
