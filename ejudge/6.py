def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

n = int(input())
gen = fibonacci()
if n == 0:
    print(" ")
else:
    for i in range(n-1):
        if i != n:
            print(next(gen), end="")
            print(",", end="")
        else:
            print(next(gen))
    print(next(gen))