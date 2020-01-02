#!/bin/bash

lines="200
300
500
700
900"

for i in $lines; do
    echo "$i"
    for j in $(seq 5); do
        { time ./solution-step4 $(cat "$i/initial-conditions-no-plot.txt"); } 2> "time-2-$i-$j.txt"
    done
done
