def is_non_zero(n):
    if n == 0:
        return True
    else:
        return False
    
input()
l = list(map(int, input().split()))

result = sum(map(is_non_zero, l))
print(result)