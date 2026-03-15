input()
l = list(map(int, input().split()))

result = sorted(set(l))
result.sort()

for i in result:
    print(i, end= " ")