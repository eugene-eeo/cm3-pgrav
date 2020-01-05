r = open('t_amdahl_hamilton_large.csv')
for n, line in enumerate(r, 1):
    line = line.strip()
    mins, secs = line.split('m')
    secs = secs.rstrip('s')
    total = int(mins) * 60 + float(secs)
    print(f"{n},{total}")
