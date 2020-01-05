#!/bin/bash

nums="1
2
3
4
5
6
7
8"

# for _ in $(seq 5); do
#     for thread_count in $nums; do
#         if [ "$thread_count" = 1 ]; then
#             echo -n "1,"
#             command time -f '%e' ./solution-step1 $(cat 8/initial-conditions-no-plot.txt) 1> /dev/null
#         else
#             echo -n "$thread_count,"
#             OMP_NUM_THREADS="$thread_count" command time -f '%e' ./solution-step4 $(cat 8/initial-conditions-no-plot.txt) 1> /dev/null
#         fi
#     done
# done

echo "serial"
for _ in $(seq 5); do
    for thread_count in $nums; do
        echo -n "$thread_count,"
        command time -f '%e' ./solution-step1 $(cat "cond-cores-$thread_count.txt") 1> /dev/null
    done
done

echo "parallel"
for _ in $(seq 5); do
    for thread_count in $nums; do
        echo -n "$thread_count,"
        OMP_NUM_THREADS="$thread_count" command time -f '%e' ./solution-step4 $(cat "cond-cores-$thread_count.txt") 1> /dev/null
    done
done
