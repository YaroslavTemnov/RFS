def even(i):
    if int(i) % 2 == 0:
        return True
    else:
        return False



n = input()
l = [x for x in input().split()]

result = len(list(filter(even, l)))

print(result)