import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

info = [
    (1, 19.976),
    (2, 14.855),
    (3, 12.3),
    (4, 10.818000000000001),
    (5, 9.378),
    (6, 9.0175),
    (7, 8.942),
    (8, 8.56),
]

# info = [
#     (1, 112.66),
#     (2, 100.36),
#     (3, 77.176),
#     (4, 64.736),
#     (5, 62.962),
#     (6, 55.098),
#     (7, 48.806),
#     (8, 44.17),
# ]

# info = [
#     (1, 19.976),
#     (2, 17.582),
#     (3, 14.4),
#     (4, 13.004),
#     (5, 11.936),
#     (6, 10.358),
#     (7, 9.44),
#     (8, 8.982),
# ]

x = [u[0] for u in info]
t = [u[1] for u in info]


def amdahl(p, f):
    return f * t[0] + (1 - f) * t[0] / p


popt, pcov = curve_fit(amdahl, x, t)
[f] = popt

plt.scatter(x, t, c='b', label='data')
plt.scatter(x, amdahl(x, *popt), c='r', label='fit: f=%5.3f' % tuple(popt))
plt.xlabel('nproc')
plt.ylabel('t')
plt.legend()
plt.show()
