import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

timing = [
    (1, 290.894),
    (2, 272.826),
    (2, 269.556),
    (2, 273.233),
    (2, 266.801),
    (2, 270.397),
    (4, 141.941),
    (4, 140.973),
    (4, 138.99),
    (4, 134.222),
    (4, 139.685),
    (6, 104.071),
    (6, 104.09),
    (6, 102.132),
    (6, 104.262),
    (6, 104.14500000000001),
    (8, 77.89099999999999),
    (8, 78.538),
    (8, 79.176),
    (8, 79.116),
    (8, 76.55799999999999),
    (10, 63.565),
    (10, 62.552),
    (10, 62.88),
    (10, 62.724000000000004),
    (10, 62.991),
    (12, 53.3),
    (12, 52.94),
    (12, 52.831),
    (12, 52.584),
    (12, 52.341),
    (14, 46.592),
    (14, 46.5),
    (14, 46.669),
    (14, 45.791),
    (14, 46.492),
    (16, 40.938),
    (16, 40.805),
    (16, 40.384),
    (16, 40.731),
    (16, 41.26),
    (18, 36.102),
    (18, 36.534),
    (18, 36.528),
    (18, 35.72),
    (18, 36.803),
    (20, 33.029),
    (20, 32.262),
    (20, 32.374),
    (20, 32.421),
    (20, 32.431),
    (22, 29.386),
    (22, 29.819),
    (22, 29.839),
    (22, 29.717),
    (22, 29.974),
    (24, 26.977),
    (24, 26.836),
    (24, 26.883),
    (24, 26.947),
    (24, 26.893),
]


def main():
    infos = {}
    info = {}

    for u, t in timing:
        if u not in infos:
            infos[u] = []
        infos[u].append(t)

    for u, v in infos.items():
        info[u] = sum(v) / len(v)

    speedup = {}
    for k in info:
        speedup[k] = info[1] / info[k]

    print(speedup)

    xdata = np.array(sorted(speedup.keys()))
    ydata = np.array([speedup[k] for k in xdata])

    # xdata = np.array(sorted(info.keys()))
    # ydata = np.array([info[k] for k in xdata])

    # def amdahl(p, f):
    #     return info[1] * f + (1 - f) * info[1] / p

    def amdahl(p, f):
        return 1 / (f + (1 - f) / p)

    [f], _ = curve_fit(amdahl, xdata, ydata)
    plt.scatter(xdata, ydata, c='b', label='data')
    plt.scatter(xdata, amdahl(xdata, f), c='r', label='fit: f=%5.3f' % f)
    plt.grid()
    plt.xlabel('cores')
    plt.ylabel('speedup')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
