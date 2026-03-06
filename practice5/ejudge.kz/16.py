import re

s = input()

pattern = r"Name:\s*([A-Za-z]+), \s*Age:\s(\d+)"

result = re.search(pattern, s)

print(f"{result.group(1)}{result.group(2)}")