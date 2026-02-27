def squares(n):
    for i in range(n+1):
        yield i ** 2


n = int(input())

result = squares(n)

for i in result:
    print(i)