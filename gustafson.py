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
            mins, secs = time.split('m')
            secs = secs.rstrip('s')
            total = int(mins) * 60 + float(secs)
            # if int(nproc) > 24:
            #     continue
            mode[int(nproc)].append(total)

    s = {k: avg(v) for k, v in serial.items()}
    p = {k: avg(v) for k, v in parallel.items()}

    speedup = {}
    for k in s:
        speedup[k] = s[k] / p[k]

    print(speedup)

    xdata = np.array(sorted(speedup.keys()))
    ydata = np.array([speedup[k] for k in xdata])

    def gustafson(p, f):
        return f + (1 - f) * p

    my_dpi = 96
    plt.figure(figsize=(400/my_dpi, 400/my_dpi), dpi=my_dpi)
    [f], _ = curve_fit(gustafson, xdata, ydata)

    plt.scatter(xdata, ydata, c='k', marker='x', label='data')
    #plt.plot(xdata, ydata, 'kx-', label='data')
    plt.plot(xdata, gustafson(xdata, f), 'kx-', label='fit: f=%5.3f' % f, alpha=0.3)
    plt.grid()
    plt.title('Weak Scaling')
    plt.xlabel('cores')
    plt.ylabel('scaled speedup')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()

    # plt.savefig('speedups-more2.png', dpi=my_dpi * 2)
    plt.show()


if __name__ == '__main__':
    main()
