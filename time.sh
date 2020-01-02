#!/bin/bash

lines="6
7
8
9
10
11
12
13"

for i in $lines; do
    echo "$i"
    for j in $(seq 5); do
        { time ./solution-step4 $(cat "$i/initial-conditions-no-plot.txt"); } 2> "timing/time-$i-$j.txt"
    done
done
