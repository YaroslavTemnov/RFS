def only_even():
    a = 0
    while True:
        yield a
        a += 2
        
n = int(input())
res = only_even()
for i in range(int(n/2 + 1)):
    if i != int(n/2):
        print(next(res), end ="")
        print(",", end = "")
    else:
        print(next(res), end="")