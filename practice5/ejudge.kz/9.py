import re

s = input()

result = re.findall("\\b[a-zA-Z]{3}\\b", s)

print(len(result))