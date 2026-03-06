import re

s = input()

result = re.findall("\\w+", s)

print(len(result))