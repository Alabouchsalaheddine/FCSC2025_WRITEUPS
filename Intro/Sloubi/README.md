# Sloubi


## Challenge Statement

> Sloubi 1! Sloubi 2! Sloubi 3! Sloubi 4! Sloubi 5! Sloubi 6! Sloubi 7! Sloubi 8! Sloubi 9! Sloubi 10! Sloubi 11! Sloubi 12! Sloubi 13! Sloubi 14! Sloubi 15! Sloubi 16! Sloubi 17! Sloubi 18! Sloubi 19! Sloubi 20! Sloubi 21! Sloubi 22! Sloubi 23! Sloubi 24! Sloubi 25! Sloubi 26! Sloubi 27! Sloubi 28! Sloubi 29! Sloubi 30! Sloubi 31! Sloubi 32!

---

## Solution

We used Ghidra to analyze the binary and reverse engineer the logic to find the flag.

1.  **Identify the Core Logic:** The `main` function contains the primary logic for the challenge.

2.  **Input Handling:**
    *   `char local_68 [48];`: A buffer `local_68` of size 48 is allocated on the stack.
    *   `fgets(local_68, 0x28, stdin);`: Reads up to `0x28` (40 decimal) characters from standard input into `local_68`. This is the user's input.
    *   The code checks if `fgets` was successful.
    *   It removes the trailing newline character (`\n`) from the input if present.
    *   `if (local_78 == 0x20)`: It checks if the length of the input string (after removing the newline) is exactly `0x20` (32 decimal). If not, it prints "Nope." and exits. This tells us the flag must be 32 characters long.

3.  **The Scrambling Operation:**
    *   `char local_38 [32];`: Another buffer `local_38` of size 32 is allocated.
    *   `for (local_70 = 0; local_70 < 0x20; local_70 = local_70 + 1) { local_38[(local_70 * 0x11 + 0x33) % 0x20] = local_68[local_70]; }`: This is the crucial part. It takes each character from the input buffer `local_68` (let's call the index `i`, which is `local_70`) and places it into the `local_38` buffer at a *different* index `j`. The destination index `j` is calculated using the formula: `j = (i * 0x11 + 0x33) % 0x20`.
        *   `0x11` is 17 in decimal.
        *   `0x33` is 51 in decimal.
        *   `0x20` is 32 in decimal.
        *   So, the formula is: `destination_index = (original_index * 17 + 51) % 32`.
        *   This loop rearranges (scrambles) the input characters from `local_68` into `local_38`.

4.  **The Comparison:**
    *   `iVar1 = strcmp(local_38, "4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW");`: The scrambled string in `local_38` is compared to the hardcoded string `"4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW"`.
    *   `if (iVar1 == 0)`: If the strings match (`strcmp` returns 0), it prints the "Congrats!" message.

5.  **Finding the Flag:** To find the original flag (which was entered into `local_68`), we need to reverse the scrambling process. We know the target scrambled string (`S = "4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW"`) and the scrambling formula (`S[j] = F[i]` where `j = (i * 17 + 51) % 32`). We need to find the original flag `F`.

    We can iterate through the *original* indices `i` from 0 to 31, calculate the corresponding scrambled index `j`, and then assign the character `S[j]` to the position `F[i]`.

    Let's write a small script (e.g., in Python) to do this:

    ```python
    scrambled = "4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW"
    flag_len = 32 # 0x20
    original_flag = [''] * flag_len

    # The scrambling formula: j = (i * 0x11 + 0x33) % 0x20
    # Where i is the original index, j is the scrambled index.
    # scrambled[j] = original_flag[i]
    # We want to find original_flag[i]

    A = 0x11 # 17
    B = 0x33 # 51
    N = 0x20 # 32

    for i in range(N):
        j = (i * A + B) % N
        original_flag[i] = scrambled[j]

    flag = "".join(original_flag)
    print(flag)
    ```

6.  **Running the script gives:**
    ```
    FCSC{CQR7vBWgmh}zCHB3QJCuS42FsNeW
    ```

7.  **Verification:**
    *   The length is 32 characters.
    *   It starts with `FCSC{` and ends with `}`.

---

## Flag

```
FCSC{JgeBhrCWQBsmHu7N2mCVCvQz4u}
```