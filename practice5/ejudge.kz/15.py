import re

s = input()

def double_digit(match):
    digit = match.group(0)
    return digit * 2

result = re.sub("\\d", double_digit, s)

print(result)