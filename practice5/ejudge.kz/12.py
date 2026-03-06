import re

s = input()

result = re.findall("[0-9]{2,}", s)

for i in result:
    print(i, end = " ")