import re

s = input()

result = re.findall("[0-3][0-9]/[0-1][0-9]/[0-9][0-9]", s)

print(len(result))