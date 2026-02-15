def is_even(n):
    tp = 0
    for i in n:
        if int(i) % 2 == 0:
            tp += 1
        else:
            return "Not valid"
        
    return "Valid"


n = input()
print(is_even(n))