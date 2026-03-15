input()
a = [x for x in input().split()]
b = [x for x in input().split()]
c = input()

res = zip(a, b)
value = False
pos = 0

for i in res:
    if c in i:
        value = True
        pos = i[1]
        break
    else:
        continue

if value:
    print(pos)
else:
    print("Not found")