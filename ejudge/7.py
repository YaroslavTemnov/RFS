input()

l = [x for x in input().split()]
result = max(l, key = len)

print(result)