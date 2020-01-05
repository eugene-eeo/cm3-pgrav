#!/bin/bash
for _ in $(seq "$1"); do
    time OMP_NUM_THREADS=$1 ./solution-step4 $(cat setups/setup-4.txt)
done
