#!/usr/bin/env python3
from pwn import *
import random

def solve(A):
    max_sum = current_sum = A[0]
    start = end = temp_start = 0

    for i in range(1, len(A)):
        if current_sum < 0:
            current_sum = A[i]
            temp_start = i
        else:
            current_sum += A[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i + 1

    return max_sum, start, end

HOST = args.HOST or "chall.fcsc.fr"
PORT = args.PORT or 2050
io = remote(HOST, PORT)

try:
    while True:
        line = io.recvline().decode()
        if "(seed, n, N)" not in line:
            print(line.strip())
            continue

        # Parse seed, n, N
        print(line.strip())
        exec(line.strip())  # sets (seed, n, N)

        # Regenerate A with the given seed
        random.seed(seed)
        A = [random.randrange(-n, n) for _ in range(2 ** N)]

        # Solve max subarray sum
        m, i, j = solve(A)

        # Send i
        io.sendlineafter(b">>> i = ", str(i).encode())

        # Send j
        io.sendlineafter(b">>> j = ", str(j).encode())

except EOFError:
    print("[+] Connection closed")
    io.close()
