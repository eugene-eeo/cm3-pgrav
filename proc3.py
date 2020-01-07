lines = """179,0m32.408s
64,0m29.745s
134,0m31.613s
199,0m32.545s
39,0m26.435s
34,0m29.229s
124,0m31.783s
189,0m32.511s
184,0m32.460s
139,0m31.723s
44,0m26.356s
174,0m31.993s
144,0m31.140s
94,0m29.659s
104,0m30.844s
69,0m29.439s
129,0m31.295s
24,0m21.022s
89,0m30.411s
149,0m32.080s
74,0m29.202s
169,0m32.268s
84,0m29.834s
114,0m31.567s
29,0m33.818s
164,0m31.865s
159,0m32.019s
54,0m28.753s
49,0m30.351s
154,0m31.639s
99,0m30.316s
194,0m32.370s
79,0m29.356s
109,0m31.060s
119,0m31.560s
59,0m29.269s"""


r = iter(lines.splitlines())

for line in r:
    line = line.strip()
    n, line = line.split(',', 1)
    mins, secs = line.split('m')
    secs = secs.rstrip('s')
    total = int(mins) * 60 + float(secs)
    print(f"({n},{total}),")
