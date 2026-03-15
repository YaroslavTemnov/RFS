def square(i):
    return i**2

n = input()
l = [x for x in input().split()]

result = sum(list(map(square, l)))

print(result)