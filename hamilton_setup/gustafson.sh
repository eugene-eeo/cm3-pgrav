#!/bin/bash

cd eeojun
time ./solution-step1 $(cat setups/setup-$1.txt)
time OMP_NUM_THREADS=$1 ./solution-step4 $(cat setups/setup-$1.txt)
