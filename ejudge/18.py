import sys

data = sys.stdin.read().split()

x1 = float(data[0])
y1 = float(data[1])
x2 = float(data[2])
y2 = float(data[3])

dy = y1 + y2

if abs(dy) < 1e-12:

    x = (x1 + x2) / 2
else:
    t = y1 / dy
    x = x1 + t * (x2 - x1)

print("%.10f %.10f" % (x, 0))