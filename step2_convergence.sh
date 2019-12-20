#!/bin/bash
# shellcheck disable=2086

params="0 0 0 0 0 0 4 3 0 0 0 0 0 5 3 4 0 0 0 0 3"
echo "1e-6"
./solution-step2 0 100 1e-6 $params
echo "5e-7"
./solution-step2 0 100 5e-7 $params
echo "1e-7"
./solution-step2 0 100 1e-7 $params
echo "5e-8"
./solution-step2 0 100 5e-8 $params
echo "1e-8"
./solution-step2 0 100 1e-8 $params
echo "5e-9"
./solution-step2 0 100 5e-9 $params

echo -n "1e-6, "         && ./solution-step2 0 100 1e-6 $params         | tail -n 1
echo -n "0.5e-6, "       && ./solution-step2 0 100 0.5e-6 $params       | tail -n 1
echo -n "0.25e-6, "      && ./solution-step2 0 100 0.25e-6 $params      | tail -n 1
echo -n "0.125e-6, "     && ./solution-step2 0 100 0.125e-6 $params     | tail -n 1
echo -n "0.0625e-6, "    && ./solution-step2 0 100 0.0625e-6 $params    | tail -n 1
echo -n "0.03125e-6, "   && ./solution-step2 0 100 0.03125e-6 $params   | tail -n 1
echo -n "0.015625e-6, "  && ./solution-step2 0 100 0.015625e-6 $params  | tail -n 1
echo -n "0.0078125e-6, " && ./solution-step2 0 100 0.0078125e-6 $params | tail -n 1
