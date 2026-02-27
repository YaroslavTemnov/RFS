def limited_cycle(items, k):
    for _ in range(k):
        for item in items:
            yield item



items = input().split()
k = int(input())

gen = limited_cycle(items, k)

print(' '.join(gen))