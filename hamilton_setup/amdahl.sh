#!/bin/bash
for _ in $(seq 5); do
    time OMP_NUM_THREADS=$1 ./solution-step4 $(cat setups/setup-24.txt)
done
