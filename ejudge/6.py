def ispos(i):
    if int(i) >= 0:
        return True
    else:
        return False
    
n = input()
l = [x for x in input().split()]
check = list(map(ispos, l))

if all(check):
    print("Yes")
else:
    print("No")