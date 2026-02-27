def back_count(n):
    for i in range(n + 1):
        yield n - i
    

n = int(input())
res = back_count(n)
for i in res:
    print(i)