import math

a = int(input())      
b = float(input())    

area = (a * b**2) / (4 * math.tan(math.pi / a))

print(f"{area:.0f}")