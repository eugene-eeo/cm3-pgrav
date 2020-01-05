import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


amdahl_speedup = {1: 1.0, 2: 1.0751449017713461, 4: 2.0903233780437507, 6: 2.8040678619625985, 8: 3.7172196821194086, 10: 4.621590533567198, 12: 5.509439536962682, 14: 6.268078467876782, 16: 7.125633212161593, 18: 8.005360867866166, 20: 8.949648344480886, 22: 9.778935690994052, 24: 10.811009692572991}  # noqa: E501
gustafson_speedup = {1: 0.562519842169713, 2: 0.9724672228843861, 4: 2.0318071482380518, 6: 2.9072032709343807, 8: 3.712294428197045, 10: 4.420048864092186, 12: 5.326490964407464, 14: 6.400356797740281, 16: 6.951672462625031, 18: 8.002738425587848, 20: 8.898545401116662, 22: 9.686723729739574, 24: 10.801667593107283}  # noqa: E501


def amdahl(p, f):
    return 1 / (f + (1 - f) / p)


def gustafson(p, f):
    return f + (1 - f) * p


def main():
    amdahl_xdata = np.array(list(amdahl_speedup.keys()))
    amdahl_ydata = np.array(list(amdahl_speedup.values()))

    gustafson_xdata = np.array(list(gustafson_speedup.keys()))
    gustafson_ydata = np.array(list(gustafson_speedup.values()))

    [f_a], _ = curve_fit(amdahl, amdahl_xdata, amdahl_ydata)
    [f_g], _ = curve_fit(gustafson, gustafson_xdata, gustafson_ydata)

    plt.subplot(1, 2, 1)
    plt.title('Strong Scaling')
    plt.plot(amdahl_xdata, amdahl_ydata, 'ko-', label='data')
    plt.plot(amdahl_xdata, amdahl(amdahl_xdata, f_a), 'ro-',
             label='fit: f=%5.3f' % f_a)
    plt.grid()
    plt.xlabel('Threads')
    plt.ylabel('Speedup')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Weak Scaling')
    plt.plot(gustafson_xdata, gustafson_ydata, 'ko-', label='data')
    plt.plot(gustafson_xdata, gustafson(gustafson_xdata, f_g), 'ro-',
             label='fit: f=%5.3f' % f_g)
    plt.grid()
    plt.xlabel('Threads')
    plt.ylabel('Speedup')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
