import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dist1 = math.hypot(x1, y1)
dist2 = math.hypot(x2, y2)

if dist1 < R:
    dist1 = R
if dist2 < R:
    dist2 = R

if dist1 >= R and dist2 >= R:
    dot = x1 * x2 + y1 * y2
    cos_theta = dot / (dist1 * dist2)
    cos_alpha = R / dist1
    cos_beta = R / dist2
    
    if cos_theta >= cos_alpha * cos_beta - math.sqrt((1 - cos_alpha**2) * (1 - cos_beta**2)):
        dist = math.hypot(x2 - x1, y2 - y1)
        print(f"{dist:.10f}")
    else:

        theta = math.acos(cos_theta)
        alpha = math.acos(cos_alpha)
        beta = math.acos(cos_beta)
        
        tangent1 = math.sqrt(dist1**2 - R**2)
        tangent2 = math.sqrt(dist2**2 - R**2)
        
        arc_length = R * (theta - alpha - beta)
        
        result = tangent1 + tangent2 + arc_length
        print(f"{result:.10f}")
else:

    dist = math.hypot(x2 - x1, y2 - y1)
    print(f"{dist:.10f}")