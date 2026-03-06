import re

s = input()

pattern = re.compile(r'^\d+$')
if pattern.fullmatch(s):
    print("Match")
else:
    print("No match")