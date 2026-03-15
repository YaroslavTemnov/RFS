def div_by_3(i):
    if i % 3 == 0:
        return i

some_list = map(int, input().split())

result_list = filter(div_by_3, some_list)

for i in result_list:
    print(i)