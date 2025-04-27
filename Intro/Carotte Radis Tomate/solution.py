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
