import re

s = input()

result = re.search("cat|dog", s)

if result:
    print("Yes")
else:
    print("No")