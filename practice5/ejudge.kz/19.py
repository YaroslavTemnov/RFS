import re

s = input()
p = re.compile(r"\b\w+\b")

result = re.findall(p, s)

print(len(result))