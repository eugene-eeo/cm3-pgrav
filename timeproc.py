import csv
import sys
from collections import defaultdict


def main():
    r = csv.reader(sys.stdin)
    next(r)

    times = defaultdict(list)
    avgs = {}

    for line in r:
        nproc, time = line
        times[int(nproc)].append(float(time))

    for nproc, timings in times.items():
        avgs[nproc] = sum(timings) / len(timings)

    print("nproc,time")
    for nproc, time in avgs.items():
        print("{},{}".format(nproc, time))


if __name__ == '__main__':
    main()
