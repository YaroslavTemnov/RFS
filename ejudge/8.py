def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    for i in range(3, int(num ** 0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def prime_generator(n):
    for num in range(2, n + 1):
        if is_prime(num):
            yield num

n = int(input())

primes = [str(p) for p in prime_generator(n)]

print(" ".join(primes))