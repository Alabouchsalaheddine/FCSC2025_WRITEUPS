# Array d'urgence

**Category**: Algorithmics / Scripting  
**Points**: 100+ points (Dynamic Scoring)

---

## Challenge Statement

You are given a classic algorithmic problem!

> nc chall.fcsc.fr 2050  
> Provided: `array-d-urgence.py`

---

## Objective

Find the subarray `A[i:j]` with the maximal sum, given that:
- A random array `A` is generated using a specific **seed** and parameters `(seed, n, N)`.
- You need to find and send back the correct `i` and `j`.

---

## Solution Strategy

1. Regenerate the exact same array `A` on your machine using the received seed and parameters.
2. Solve for the subarray with the **maximum sum** (classic Kadane's algorithm).
3. Send the correct `i` and `j` indices back to the server **very quickly** (because of time constraints).

---

## Python Script Explanation (`solution.py`)

1. **Connect to the challenge** using `pwntools`:

```python
HOST = args.HOST or "chall.fcsc.fr"
PORT = args.PORT or 2050
io = remote(HOST, PORT)
```

2. **Parse the `(seed, n, N)` parameters** received from the server:

```python
line = io.recvline().decode()
exec(line.strip())  # sets (seed, n, N)
```

3. **Regenerate the array `A`** exactly as the server did:

```python
random.seed(seed)
A = [random.randrange(-n, n) for _ in range(2 ** N)]
```

- `n` is the bound for the integers `(-n to n)`.
- `2 ** N` is the size of the array.

4. **Find the subarray with the maximal sum** using an optimized Kadane's algorithm:

```python
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
```

5. **Send the correct indices** (`i`, `j`) back to the server:

```python
io.sendlineafter(b">>> i = ", str(i).encode())
io.sendlineafter(b">>> j = ", str(j).encode())
```

6. **Repeat** the above steps for multiple rounds until the server sends the final flag.

---

## Final Flag

After successfully solving all the rounds, we obtained:

```
FCSC{b3a6e5e45a7efcbefe1757d689ad20c1b1ff886eced11b87b74bb25175efad05}
```


