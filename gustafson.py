from collections import defaultdict
import csv
import sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def avg(x):
    return sum(x) / len(x)


def main():
    file = sys.argv[1]
    r = csv.reader(open(file))

    serial = defaultdict(list)
    parallel = defaultdict(list)

    mode = serial

    for line in r:
        if line == ['serial']:
            mode = serial
        elif line == ['parallel']:
            mode = parallel
        else:
            nproc, time = line
            mode[int(nproc)].append(float(time))

    s = {k: avg(v) for k, v in serial.items()}
    p = {k: avg(v) for k, v in parallel.items()}

    speedup = {}
    for k in s:
        speedup[k] = s[k] / p[k]

    xdata = np.array(list(speedup.keys()))
    ydata = np.array(list(speedup.values()))

    def gustafson(p, f):
        return f + (1 - f) * p

    [f], _ = curve_fit(gustafson, xdata, ydata)

    plt.scatter(xdata, ydata, c='b', label='data')
    plt.scatter(xdata, gustafson(xdata, f), c='r', label='fit: f=%5.3f' % f)
    plt.xlabel('cores')
    plt.ylabel('scaled speedup')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
