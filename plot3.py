import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


amdahl_timing = dict([
    (14, 34.837),
    (14, 34.517),
    (14, 34.473),
    (14, 34.73),
    (14, 34.419),
    (1, 408.259),
    (1, 406.325),
    (1, 406.265),
    (1, 407.545),
    (1, 406.01),
    (8, 60.804),
    (8, 60.761),
    (8, 60.778),
    (8, 60.61),
    (8, 60.734),
    (12, 40.582),
    (12, 40.217),
    (12, 40.204),
    (12, 40.442),
    (12, 40.152),
    (2, 208.765),
    (2, 205.781),
    (2, 205.556),
    (2, 209.875),
    (2, 204.74099999999999),
    (7, 68.049),
    (7, 68.544),
    (7, 68.72),
    (7, 67.283),
    (7, 68.432),
    (18, 27.216),
    (18, 27.596),
    (18, 27.685),
    (18, 27.634),
    (18, 27.666),
    (11, 44.778),
    (11, 45.381),
    (11, 44.773),
    (11, 44.745),
    (11, 44.828),
    (22, 22.661),
    (22, 22.963),
    (22, 22.556),
    (22, 23.137),
    (22, 22.817),
    (20, 24.913),
    (20, 24.696),
    (20, 24.556),
    (20, 24.847),
    (20, 24.74),
    (23, 21.525),
    (23, 21.603),
    (23, 21.727),
    (23, 21.475),
    (23, 21.73),
    (21, 23.846),
    (21, 23.646),
    (21, 23.409),
    (21, 23.633),
    (21, 23.883),
    (16, 31.303),
    (16, 31.252),
    (16, 31.188),
    (16, 30.971),
    (16, 31.061),
    (3, 145.459),
    (3, 149.564),
    (3, 146.289),
    (3, 146.522),
    (3, 147.722),
    (24, 20.679),
    (24, 20.591),
    (24, 20.531),
    (24, 20.703),
    (24, 20.72),
    (4, 115.191),
    (4, 111.80799999999999),
    (4, 114.021),
    (4, 114.032),
    (4, 113.18),
    (15, 33.078),
    (15, 34.159),
    (15, 33.007),
    (15, 34.144),
    (15, 33.373),
    (6, 79.98),
    (6, 80.497),
    (6, 80.607),
    (6, 79.774),
    (6, 76.36),
    (13, 37.904),
    (13, 37.509),
    (13, 37.62),
    (13, 37.94),
    (13, 38.573),
    (19, 26.29),
    (19, 25.87),
    (19, 25.746),
    (19, 26.557),
    (19, 26.027),
    (10, 48.932),
    (10, 48.74),
    (10, 48.565),
    (10, 49.154),
    (10, 49.529),
    (5, 94.571),
    (5, 94.595),
    (5, 94.402),
    (5, 94.037),
    (5, 93.932),
    (9, 54.021),
    (9, 53.55),
    (9, 53.452),
    (9, 53.692),
    (9, 53.674),
    (17, 29.215),
    (17, 28.862),
    (17, 28.697),
    (17, 28.719),
    (17, 28.759),
])


# gustafson_speedup = {1: 0.562519842169713, 2: 0.9724672228843861, 4: 2.0318071482380518, 6: 2.9072032709343807, 8: 3.712294428197045, 10: 4.420048864092186, 12: 5.326490964407464, 14: 6.400356797740281, 16: 6.951672462625031, 18: 8.002738425587848, 20: 8.898545401116662, 22: 9.686723729739574, 24: 10.801667593107283}  # noqa: E501
gustafson_speedup = {1: 0.7276494967436352, 2: 0.923044862079418, 3: 1.7640325670498085, 4: 2.4325408767178254, 5: 2.9621108949416346, 6: 3.884193047297659, 7: 4.25263996812114, 8: 4.742593586802674, 9: 5.231256904087219, 10: 5.955312761454796, 11: 6.377089103237513, 12: 7.031131984119299, 13: 7.652911222136818, 14: 8.130455612513773, 15: 8.728516562650025, 16: 9.171586978154764, 17: 9.7630615640599, 18: 10.573149992711725, 19: 10.882004361429791, 20: 11.413049565947915, 21: 12.014502369668246, 22: 12.81874668850248, 23: 13.436601370259579, 24: 14.197367784390575}  # noqa: E501


def amdahl(p, f):
    # return amdahl_timing[1] * f + (1 - f) * amdahl_timing[1] / p
    return 1 / (f + (1 - f) / p)


def gustafson(p, f):
    return f + (1 - f) * p


def main():
    speedup = {k: amdahl_timing[1] / amdahl_timing[k] for k in amdahl_timing}

    amdahl_xdata = np.array(sorted(speedup.keys()))
    amdahl_ydata = np.array([speedup[x] for x in amdahl_xdata])
    # amdahl_xdata = np.array(sorted(amdahl_timing.keys()))
    # amdahl_ydata = np.array([amdahl_timing[x] for x in amdahl_xdata])

    gustafson_xdata = np.array(sorted(gustafson_speedup.keys()))
    gustafson_ydata = np.array([gustafson_speedup[x] for x in gustafson_xdata])

    [f_a], _ = curve_fit(amdahl, amdahl_xdata, amdahl_ydata)
    [f_g], _ = curve_fit(gustafson, gustafson_xdata, gustafson_ydata)

    my_dpi = 96
    plt.figure(figsize=(850/my_dpi, 400/my_dpi), dpi=my_dpi)

    plt.subplot(1, 2, 1)
    plt.title('Strong Scaling')
    plt.scatter(amdahl_xdata, amdahl_ydata, c='k', marker='x', label='data')
    plt.plot(amdahl_xdata, amdahl(amdahl_xdata, f_a), 'kx-',
             label='fit: f=%5.3f' % f_a, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Threads')
    plt.ylabel('Speedup')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Weak Scaling')
    plt.scatter(gustafson_xdata, gustafson_ydata, c='k', marker='x', label='data')
    plt.plot(gustafson_xdata, gustafson(gustafson_xdata, f_g), 'kx-',
             label='fit: f=%5.3f' % f_g, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Threads')
    plt.ylabel('Scaled Speedup')
    plt.legend()

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    plt.savefig('speedups.png', dpi=my_dpi)


if __name__ == '__main__':
    main()
