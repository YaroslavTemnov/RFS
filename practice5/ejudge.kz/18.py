import re

s = input()
p = input()

result = re.findall(re.escape(p), s)

print(len(result))