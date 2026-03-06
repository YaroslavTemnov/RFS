import re

s = input()
p = input()

if re.search(p, s):
    print("Yes")
else:
    print("No")