def power(n):
  return lambda a : a ** n

n = int(input())
square = power(2)
print(square(n))