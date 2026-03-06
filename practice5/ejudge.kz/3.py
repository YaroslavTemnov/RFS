import re

s = input()
p = input()

print(len(re.findall(p, s)))