from math import sqrt
def isUsual(a):
    if a < 2:
        return False
    
    for i in range(2, int(sqrt(a))+1):
        if a % i == 0:
            return False
    
    return True




n = list(map(int, input().split()))

result = list(filter(lambda x: isUsual(x), n))
if result:
    for i in result:
        print(i, end=" ")
else:
    print("No primes")