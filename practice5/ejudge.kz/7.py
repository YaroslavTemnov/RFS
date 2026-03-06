import re

s = input()
p = input()
r = input()
result = re.sub(p, r, s)

print(result)