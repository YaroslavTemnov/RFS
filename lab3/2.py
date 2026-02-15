def isUsual(n):
    while n != 1:
        if n % 2 == 0:
            n = int(n/2)
        elif n % 3 == 0:
            n = int(n/3)
        elif n % 5 == 0:
            n = int(n/5)
        else:
            return False

    return True

n = int(input())

if isUsual(n): print("Yes")
else: print("No")