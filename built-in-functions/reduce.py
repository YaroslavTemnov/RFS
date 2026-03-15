from functools import reduce


some_list = [x for x in input().split()]

result_list = reduce(lambda a, b: int(a)**2 + int(b)**2, some_list)

print(result_list)

