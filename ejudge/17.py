import sys
import math

input = sys.stdin.read
data = input().split()


R = float(data[0])
x1, y1 = float(data[1]), float(data[2])
x2, y2 = float(data[3]), float(data[4])


dx = x2 - x1
dy = y2 - y1
total_length = math.sqrt(dx*dx + dy*dy)

if total_length < 1e-9:

    dist = math.sqrt(x1*x1 + y1*y1)
    print("%.10f" % (total_length if dist <= R + 1e-9 else 0.0))
    sys.exit(0)


ux = dx / total_length
uy = dy / total_length

t = - (x1 * ux + y1 * uy)

dist_to_line = math.sqrt(max(0.0, x1*x1 + y1*y1 - t*t))

if dist_to_line > R + 1e-9:
    print("%.10f" % 0.0)
    sys.exit(0)

half_chord = math.sqrt(max(0.0, R*R - dist_to_line*dist_to_line))

t_enter = t - half_chord
t_exit  = t + half_chord

t_start = max(0.0, t_enter)
t_end   = min(total_length, t_exit)

length_inside = max(0.0, t_end - t_start)
print("%.10f" % length_inside)