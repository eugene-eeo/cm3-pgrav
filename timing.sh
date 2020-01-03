#!/bin/bash

nums="1
2
3
4
5
6
7
8"

# for thread_count in $nums; do
#     if [ "$thread_count" = 1 ]; then
#         for _ in $(seq 5); do
#             echo -n "1,"
#             command time -f '%e' ./solution-step1 $(cat 6/initial-conditions-no-plot.txt) 1> /dev/null
#         done
#     else
#         for _ in $(seq 5); do
#             echo -n "$thread_count,"
#             OMP_NUM_THREADS="$thread_count" command time -f '%e' ./solution-step4 $(cat 6/initial-conditions-no-plot.txt) 1> /dev/null
#         done
#     fi
# done

for thread_count in $nums; do
    num=$(( thread_count + 5 ));
    if [ "$thread_count" = 1 ]; then
        for _ in $(seq 5); do
            echo -n "1,"
            command time -f '%e' ./solution-step1 $(cat "$num/initial-conditions-no-plot.txt") 1> /dev/null
        done
    else
        for _ in $(seq 5); do
            echo -n "$thread_count,"
            OMP_NUM_THREADS="$thread_count" command time -f '%e' ./solution-step4 $(cat "$num/initial-conditions-no-plot.txt") 1> /dev/null
        done
    fi
done
