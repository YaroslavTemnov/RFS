def powers_of_two(n):
    power = 1          
    for i in range(n + 1):
        yield power
        power *= 2     

n = int(input())

result = [str(p) for p in powers_of_two(n)]

print(" ".join(result))