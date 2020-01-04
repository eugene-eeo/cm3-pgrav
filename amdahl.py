import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def main():
    info = dict([
        (1, 19.976),
        (2, 14.835999999999999),
        (3, 12.518),
        (4, 10.988),
        (5, 9.492),
        (6, 8.983999999999998),
        (7, 8.803999999999998),
        (8, 8.556000000000001),
    ])

    speedup = {}
    for k in info:
        speedup[k] = info[1] / info[k]

    xdata = np.array(list(speedup.keys()))
    ydata = np.array(list(speedup.values()))

    def amdahl(p, f):
        return 1 / (f + (1 - f) / p)

    [f], _ = curve_fit(amdahl, xdata, ydata)
    plt.scatter(xdata, ydata, c='b', label='data')
    plt.scatter(xdata, amdahl(xdata, f), c='r', label='fit: f=%5.3f' % f)
    plt.xlabel('cores')
    plt.ylabel('speedup')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
