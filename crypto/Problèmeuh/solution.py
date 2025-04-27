from math import isqrt
from hashlib import sha256

def is_pentagonal(n):
    # Solves 3y^2 - y - 2n = 0 → discriminant D = 1 + 24n must be perfect square
    D = 1 + 24 * n
    sqrt_D = isqrt(D)
    return sqrt_D * sqrt_D == D and (1 + sqrt_D) % 6 == 0

for c in range(1, 10**11):
    a = 487 * c
    if (159 * a) % 485 != 0:
        continue
    b = (159 * a) // 485
    x2 = a + b
    x = isqrt(x2)
    if x * x != x2:
        continue
    if not is_pentagonal(b * 2):
        continue
    y = (1 + isqrt(1 + 24 * 2 * b)) // 6
    print(f"a = {a}, b = {b}, c = {c}, x = {x}, y = {y}")
    h = sha256(str(a).encode()).hexdigest()
    print(f"FCSC{{{h}}}")
    break


