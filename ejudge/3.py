n = input()
l = [x for x in input().split()]

result = enumerate(l, 0)

for i in result:
    print(str(i[0]), + ":" + str(i[1]), end= " ")