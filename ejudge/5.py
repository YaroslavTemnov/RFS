def isvowel (i):
    if i in ['i', 'o', 'u', 'a', 'e', 'A', 'U', 'O', 'E', 'I']:
        return True
    else:
        return False
    
s = input()
check = list(map(isvowel, s))
if any(check):
    print("Yes")
else:
    print("No")