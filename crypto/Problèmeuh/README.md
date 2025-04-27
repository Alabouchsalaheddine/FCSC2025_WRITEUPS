# Problèmeuh

**Points**: 195  
**Category**: Crypto / Math

---

## Challenge Statement

Here is a nice and small system to solve.

File provided: `problemeuh.py`

---

## Solution

```python
from math import isqrt
from hashlib import sha256

def is_pentagonal(n):
    # A number n is pentagonal if (1 + sqrt(1 + 24*n)) % 6 == 0
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
```

---

The script tries to find values of `c` that satisfy:

- \( a = 487 \times c \)
- \( b = \frac{159a}{485} \) must be an integer
- \( x^2 = a + b \) where \( x \) is an integer
- \( 2b \) must be a pentagonal number

Finally, the flag is the SHA-256 hash of the value `a`.

---

## Flag

```
FCSC{b313c611e23a09e5479b10793705fb40a7a32dbcbd8c4bc2b1a33e42c4579cae}
```


