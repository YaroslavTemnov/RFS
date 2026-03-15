n = input()
a = [x for x in input().split()]
b = [x for x in input().split()]

pairs = zip(a, b)
result = 0
for i in pairs:
    resut += int(i[0]) * int(i[1])

print(result)