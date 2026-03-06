import re

s = input()
p = input()

result = re.split(p, s)

for i in range(0, len(result)):
    if i == len(result)-1:
        print(result[i])
    else:
        print(result[i],end=",")