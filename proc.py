import csv
import sys
import math


def distance(x0, y0, z0, x1, y1, z1):
    return math.sqrt(
        (x0 - x1) * (x0 - x1) +
        (y0 - y1) * (y0 - y1) +
        (z0 - z1) * (z0 - z1)
    )


def main():
    r = csv.reader(sys.stdin)
    next(r)
    # first
    _, x0, y0, z0, x1, y1, z1 = next(r)
    x0 = float(x0)
    y0 = float(y0)
    z0 = float(z0)
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)

    _, ox0, oy0, oz0, ox1, oy1, oz1 = next(r)
    ox0 = float(ox0)
    oy0 = float(oy0)
    oz0 = float(oz0)
    ox1 = float(ox1)
    oy1 = float(oy1)
    oz1 = float(oz1)

    print("timestep,distance")
    # others
    for i, tup in enumerate(r):
        timestep, nx0, ny0, nz0, nx1, ny1, nz1 = tup
        nx0 = float(nx0)
        ny0 = float(ny0)
        nz0 = float(nz0)
        nx1 = float(nx1)
        ny1 = float(ny1)
        nz1 = float(nz1)
        if i % 2 == 0:
            print("{},{}".format(
                timestep,
                distance(x0, y0, z0, nx0, ny0, nz0) +
                distance(x1, y1, z1, nx1, ny1, nz1),
            ))
        else:
            print("{},{}".format(
                timestep,
                distance(ox0, oy0, oz0, nx0, ny0, nz0) +
                distance(ox1, oy1, oz1, nx1, ny1, nz1),
            ))


if __name__ == '__main__':
    main()
