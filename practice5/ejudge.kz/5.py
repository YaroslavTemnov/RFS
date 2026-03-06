import re

s = input()

if re.match("^[A-Za-z].+[0-9]$", s):
    print("Yes")
else:
    print("No")