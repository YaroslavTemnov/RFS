import re

s = input()

result = re.findall("[A-Z]", s)

print(len(result))