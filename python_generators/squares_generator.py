def squares(a, b):
    while a <= b:
        yield a ** 2
        a += 1
        
a, b = list(map(int, input().split()))
res = squares(a, b)
for i in range(b-a + 1):
    print(next(res))