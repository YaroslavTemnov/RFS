def divisible(n):
    a = 0
    while a * 3 * 4 <= n:
        yield a * 3 * 4
        a += 1


n = int(input())
res = divisible(n)
for i in res:
    print(i, end=" ")