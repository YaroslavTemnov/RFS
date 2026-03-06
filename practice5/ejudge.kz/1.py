import re

s = input()

if re.match("^Hello", s):
    print("Yes")
else:
    print("No")