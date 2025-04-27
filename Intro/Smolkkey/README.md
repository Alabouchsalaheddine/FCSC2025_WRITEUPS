
# Smölkkey


## Challenge Statement

No statement provided.

---

## Solution


You're given:
- RSA public modulus `n`
- public exponent `e = 3`
- ciphertext `c`
- the encryption function is `c = m^e mod n`
- and you know `m` was converted from a file (`flag.txt`) via `int.from_bytes(..., "little")`.

The **key insight** is that **`e = 3` is very small**, and if the message `m` is **small enough** such that:

```text
m^3 < n
```

Then **modular reduction doesn't actually happen**, and `c = m^3` **exactly**, so:

```python
m = round(c ** (1/3))
```

This is the **low exponent vulnerability** of RSA.

---

### ✅ Steps to solve:

You need to compute the **integer cube root** of `c` to recover `m`, then convert it back to bytes.

Here’s a Python script to do that:

```python
from Crypto.Util.number import long_to_bytes
import gmpy2

# Provided values
c = 6317668510138686569655374990729607736156413707292408158720036346854309670467296052918552527575331589363290061240725095262980389263184520673983411112154423282089471021996509038472493779143273789325774414352608726252566350689111876373836913240644190951995980896093509379920452743478551321978067299216590452459233562642920123055978471365092000347562228787318105538018723376505390423730687522026043802357456368003656219942603097205774742385485995835519133581552096067468551713114231926639878045212204590071768

# Step 1: Cube root
m = int(gmpy2.iroot(c, 3)[0])  # [0] gives root, [1] tells if it was exact

# Step 2: Convert back to bytes (remember it's "little"-endian)
flag_bytes = m.to_bytes((m.bit_length() + 7) // 8, "little")

# Step 3: Print flag
print(flag_bytes.decode(errors="ignore"))
```


---

## Flag

```
FCSC{30f7c4b2fa7f0fb48bfbd9bbd413491c0a6da660764961b862fe38a83b4bc00f}
```
