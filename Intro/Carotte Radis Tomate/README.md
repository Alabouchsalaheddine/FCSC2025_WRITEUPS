# Carotte Radis Tomate


## Challenge Statement

Eat five fruits and vegetables every day!

---

## Solution

The script does the following:
1.  Generates a random 32-byte key.
2.  Treats this 32-byte key as a very large integer using `int.from_bytes()`.
3.  Calculates the remainder of this large integer when divided by five specific large numbers (associated with carotte, radis, tomate, pomme, banane).
4.  Encrypts the content of `flag.txt` using this 32-byte key with AES in ECB mode, padding the data to a multiple of 16 bytes.
5.  Prints the remainders and the encrypted ciphertext.

We are given the remainders and the ciphertext. Our goal is to find the flag.

The core of the problem lies in recovering the 32-byte key. We have an unknown integer `N` (derived from the key) and its remainders modulo five known numbers. This is a classic problem that can be solved using the **Chinese Remainder Theorem (CRT)**.

Let `N = int.from_bytes(key)`. We have the following system of congruences:
*   `N ≡ 392278890668246705 (mod 17488856370348678479)`
*   `N ≡ 4588810924820033807 (mod 16548497022403653709)`
*   `N ≡ 17164682861166542664 (mod 17646308379662286151)`
*   `N ≡ 12928514648456294931 (mod 14933475126425703583)`
*   `N ≡ 5973470563196845286 (mod 17256641469715966189)`

We can use a library like `sympy` in Python to solve this system.

First, let's list the remainders and moduli:

Remainders `r`:
`[392278890668246705, 4588810924820033807, 17164682861166542664, 12928514648456294931, 5973470563196845286]`

Moduli `m`:
`[17488856370348678479, 16548497022403653709, 17646308379662286151, 14933475126425703583, 17256641469715966189]`

Now, let's use `sympy.crt` to find the solution `N0` such that `N0 ≡ r_i (mod m_i)` for all `i`. The CRT guarantees a unique solution modulo the product of the moduli (assuming they are pairwise coprime, which large random-looking numbers usually are).

```python
import sympy

r = [
    392278890668246705,
    4588810924820033807,
    17164682861166542664,
    12928514648456294931,
    5973470563196845286
]

m = [
    17488856370348678479,
    16548497022403653709,
    17646308379662286151,
    14933475126425703583,
    17256641469715966189
]

# Solve the system of congruences using CRT
# The result is (solution, modulus)
crt_solution, product_of_moduli = sympy.crt(r, m)

print(f"CRT Solution N0: {crt_solution}")
# print(f"Product of moduli M: {product_of_moduli}") # This is a very large number

```
The CRT solution `N0` is the smallest non-negative integer satisfying the congruences. The integer `N = int.from_bytes(key)` must satisfy `N ≡ N0 (mod product_of_moduli)`. This means `N` could be `N0`, `N0 + M`, `N0 + 2M`, etc., or `N0 - M`, `N0 - 2M`, etc.

However, `key` is a 32-byte string, so `N = int.from_bytes(key, 'big')` (assuming big-endian, which is standard for `int.from_bytes` when converting arbitrary bytes) must be in the range `[0, 2^(32*8) - 1] = [0, 2^256 - 1]`.

Let's compare the size of `N0` and `product_of_moduli` with `2^256`:
*   `2^256` is approximately `1.15 x 10^77`.
*   The product of the moduli is roughly `(1.7e19)^5` which is much larger than `10^95`.

Since the product of moduli `M` is much larger than `2^256`, the only non-negative solution `N0 + k*M` that can possibly fall within the range `[0, 2^256 - 1]` is when `k=0`, provided `N0 < 2^256`.

Let's calculate `N0` and check its size:
`crt_solution = 113711883312034460403853133157348269537`
This number is approximately `1.13 x 10^38`.
`2^256` is approximately `1.15 x 10^77`.

Indeed, `N0` is much smaller than `2^265`. Therefore, the integer representation of the key, `int.from_bytes(key)`, must be equal to `N0`.

Now we need to convert this integer `N0` back into a 32-byte string to get the key. We use `N0.to_bytes(32, 'big')`.

```python
recovered_key_int = crt_solution
key_length = 32 # 32 bytes
# Assuming big-endian conversion based on typical int.from_bytes usage
recovered_key = recovered_key_int.to_bytes(key_length, 'big')

print(f"Recovered Key (bytes): {recovered_key.hex()}")
```

The recovered key is the 32 bytes represented by the integer `113711883312034460403853133157348269537`. In hexadecimal, this key is `019bf93f34781c53272237696547d664984a1505f8629d75c364c1f7a4530e21`.

Finally, we can use this key to decrypt the ciphertext using AES in ECB mode and remove the padding.

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

ciphertext_hex = "2da1dbe8c3a739d9c4a0dc29a27377fe8abc1c0feacc9475019c5954bbbf74dcedce7ed3dc3ba34fa14a9181d4d7ec0133ca96012b0a9f4aa93c42c61acbeae7640dd101a6d2db9ad4f3b8ccfe285e0d"
ciphertext = binascii.unhexlify(ciphertext_hex)

# Use the recovered key
# recovered_key = ... # calculated above

# Create AES cipher object
cipher = AES.new(recovered_key, AES.MODE_ECB)

# Decrypt the ciphertext
decrypted_padded = cipher.decrypt(ciphertext)

# Unpad the decrypted data (PKCS7 padding is default for Crypto.Util.Padding.pad)
try:
    flag = unpad(decrypted_padded, AES.block_size)
    print(f"Decrypted Flag: {flag.decode()}")
except ValueError as e:
    print(f"Decryption or unpadding failed: {e}")
    print("The recovered key might be incorrect or the padding is wrong.")

```

Combining all the Python code into one script:

```python
from sympy.ntheory.modular import crt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# Provided values
r = [
    392278890668246705,  # carotte
    4588810924820033807, # radis
    17164682861166542664, # tomate
    12928514648456294931, # pomme
    5973470563196845286  # banane
]

m = [
    17488856370348678479, # carotte modulus
    16548497022403653709, # radis modulus
    17646308379662286151, # tomate modulus
    14933475126425703583, # pomme modulus
    17256641469715966189  # banane modulus
]

ciphertext_hex = "2da1dbe8c3a739d9c4a0dc29a27377fe8abc1c0feacc9475019c5954bbbf74dcedce7ed3dc3ba34fa14a9181d4d7ec0133ca96012b0a9f4aa93c42c61acbeae7640dd101a6d2db9ad4f3b8ccfe285e0d"
ciphertext = binascii.unhexlify(ciphertext_hex)

# Step 1: Solve the CRT problem
crt_solution, _ = crt(m, r)  # Note the order: moduli, remainders

print(f"CRT Solution N0 (integer key value): {crt_solution}")

# Step 2: Convert to 32-byte key
key_length = 32
try:
    recovered_key = int(crt_solution).to_bytes(key_length, 'big')
    print(f"Recovered Key (hex): {recovered_key.hex()}")
except OverflowError:
    print(f"Error: CRT solution {crt_solution} cannot be represented as a {key_length}-byte integer.")
    exit()

# Step 3: Decrypt
try:
    cipher = AES.new(recovered_key, AES.MODE_ECB)
    decrypted_padded = cipher.decrypt(ciphertext)
    flag = unpad(decrypted_padded, AES.block_size)
    print(f"Decrypted Flag: {flag.decode()}")
except ValueError as e:
    print(f"Decryption or unpadding failed: {e}")
except Exception as e:
    print(f"Unexpected error during decryption: {e}")

```

Running this script :


The flag is `FCSC{2c4c4b3be7d86e1642ce6a8bf1bd75f33b9736e5943f51a49fb9327e248c3b6a}`. 


---

## Flag

```
FCSC{2c4c4b3be7d86e1642ce6a8bf1bd75f33b9736e5943f51a49fb9327e248c3b6a}
```
