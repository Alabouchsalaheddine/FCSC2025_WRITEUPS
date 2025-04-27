# babyfuscation

## Challenge Statement

A (very) slightly obfuscated reverse challenge!

---

## Solution


**Tools Used:** Ghidra, Python

### 1. Initial Static Analysis with Ghidra

The provided file was an ELF executable. Loading it into Ghidra and running the default analysis revealed several functions. The `main` function is the primary entry point for the program's logic.

**`main` Function Overview:**

```c
void main(void)
{
  int local_14;
  int local_10;
  int local_c;

  // Deobfuscate strings using simple XOR
  for (local_14 = 0; local_14 < 0x50; local_14 = local_14 + 1) {
    VYeXkgjLLMrczyw7i7dJPkyAbxqgCahe[local_14] = VYeXkgjLLMrczyw7i7dJPkyAbxqgCahe[local_14] ^ 0x42;
  }
  for (local_10 = 0; local_10 < 0x50; local_10 = local_10 + 1) {
    a93rEUcvwf4Ec9KHKqzFx7wL[local_10] = a93rEUcvwf4Ec9KHKqzFx7wL[local_10] ^ 0x13;
  }
  for (local_c = 0; local_c < 0x50; local_c = local_c + 1) {
    ouPrjEhgqPVNXCqchuzw7WTWLHnkbwqj[local_c] = ouPrjEhgqPVNXCqchuzw7WTWLHnkbwqj[local_c] ^ 0x37;
  }

  // Call function to get user input
  VsvYbpipYYgRoCeFtoxhtAmdFuNu3WvV();

  // Call function to transform the input
  wKtyPoT4WdyrkVzhvYUfvqo3M9iPVMd3();

  // Call function to check the transformed input and print result
  VakkEeHbtHMpNqXPMkadR4v7K();
  return;
}
```

*   **String Deobfuscation:** The program starts by deobfuscating three global character arrays using simple XOR operations. These likely correspond to the prompt message, the success message, and the failure message.
    *   `VYeXkgjLLMrczyw7i7dJPkyAbxqgCahe` XORed with `0x42`.
    *   `a93rEUcvwf4Ec9KHKqzFx7wL` XORed with `0x13`.
    *   `ouPrjEhgqPVNXCqchuzw7WTWLHnkbwqj` XORed with `0x37`.
*   **Core Logic Flow:** The program then calls three key functions in sequence:
    1.  `VsvYbpipYYgRoCeFtoxhtAmdFuNu3WvV`: Handles user input.
    2.  `wKtyPoT4WdyrkVzhvYUfvqo3M9iPVMd3`: Processes/transforms the user input.
    3.  `VakkEeHbtHMpNqXPMkadR4v7K`: Verifies the transformed input against a target value.

### 2. Analyzing Key Functions

**a) User Input (`VsvYbpipYYgRoCeFtoxhtAmdFuNu3WvV`)**

```c
void VsvYbpipYYgRoCeFtoxhtAmdFuNu3WvV(void)
{
  long lVar1;

  puts(VYeXkgjLLMrczyw7i7dJPkyAbxqgCahe); // Prints the deobfuscated prompt
  fgets(aixxj3qmUvFTqgqLodmuaEap, 0x50, stdin); // Reads user input into this buffer
  // Finds the first occurrence of newline or null byte
  lVar1 = LdUonKvqsjsJu4JdfAgtgbU9(aixxj3qmUvFTqgqLodmuaEap, &DAT_00102004); // DAT_00102004 is "\n"
  aixxj3qmUvFTqgqLodmuaEap[lVar1] = 0; // Replaces newline with null terminator
  return;
}
```

*   This function prints the prompt string (after it's been XORed).
*   It reads up to `0x50` (80) bytes of input from the user into the global buffer `aixxj3qmUvFTqgqLodmuaEap`.
*   It uses the helper function `LdUonKvqsjsJu4JdfAgtgbU9` (which behaves like `strcspn(input, "\n")`) to find the index of the newline character (`\n`) added by `fgets`.
*   It replaces the newline character with a null terminator (`\0`), effectively cleaning the input string.

**b) Input Transformation (`wKtyPoT4WdyrkVzhvYUfvqo3M9iPVMd3`)**

```c
void wKtyPoT4WdyrkVzhvYUfvqo3M9iPVMd3(void)
{
  int iVar1; // Length of input string
  int local_10; // Loop counter (i)

  // kRvUaKbhJewpX4HHFuMuPkNWc7xJ4cUV behaves like strlen
  iVar1 = kRvUaKbhJewpX4HHFuMuPkNWc7xJ4cUV(aixxj3qmUvFTqgqLodmuaEap);

  // Loop iterates from 0 up to and including the length (processes the null terminator too)
  for (local_10 = 0; local_10 < iVar1 + 1; local_10 = local_10 + 1) {
    U94y77bvL3HfcnwcAc3UA9MJTvcwjP4j[local_10] = // Output buffer
         // Part 1: Index-dependent XOR key
         (char)local_10 * '\x03' + 0x1fU ^
         // Part 2: Transformation of input character
         (aixxj3qmUvFTqgqLodmuaEap[local_10] * '\b' | // input[i] << 3
          (char)aixxj3qmUvFTqgqLodmuaEap[local_10] >> 5) // input[i] >> 5
    ;
  }
  // Ensures null termination, although the loop already processed the original null.
  U94y77bvL3HfcnwcAc3UA9MJTvcwjP4j[iVar1 + 1] = 0;
  return;
}
```

*   This is the core encryption/transformation routine.
*   It calculates the length of the input string `aixxj3qmUvFTqgqLodmuaEap` using `kRvUaKbhJewpX4HHFuMuPkNWc7xJ4cUV` (equivalent to `strlen`).
*   It iterates through the input string from index `i = 0` up to `length`. **Crucially, it also processes the null terminator at `input[length]`.**
*   For each character `input[i]` (stored in `aixxj3qmUvFTqgqLodmuaEap`), it calculates a corresponding `output[i]` (stored in `U94y77bvL3HfcnwcAc3UA9MJTvcwjP4j`).
*   The transformation formula is:
    `output[i] = ( (i * 3 + 0x1f) ^ ( (input[i] * 8) | ((char)input[i] >> 5) ) ) & 0xFF`
*   Let's analyze the `(input[i] * 8) | ((char)input[i] >> 5)` part:
    *   `input[i] * 8` is equivalent to a left bit-shift: `input[i] << 3`.
    *   `(char)input[i] >> 5` is a right bit-shift by 5.
    *   Combining these with a bitwise OR (`|`) performs a **Rotate Left (ROL)** operation by 3 bits on the 8-bit character `input[i]`.
*   So, the simplified transformation is:
    `output[i] = ((i * 3 + 0x1f) ^ ROL(input[i], 3)) & 0xFF`

**c) Verification (`VakkEeHbtHMpNqXPMkadR4v7K`)**

```c
bool VakkEeHbtHMpNqXPMkadR4v7K(void)
{
  int iVar1; // Result of comparison

  // faubPTXHmhV4vfgEpzjqfMRjJ3qunsq9 behaves like strcmp
  iVar1 = faubPTXHmhV4vfgEpzjqfMRjJ3qunsq9
                    (U94y77bvL3HfcnwcAc3UA9MJTvcwjP4j, // Transformed input
                     jMunhwoW4bRqeCdJfXvfNrRm);      // Target byte array
  if (iVar1 != 0) {
    puts(ouPrjEhgqPVNXCqchuzw7WTWLHnkbwqj); // Failure message
  }
  else {
    puts(a93rEUcvwf4Ec9KHKqzFx7wL);       // Success message
  }
  return iVar1 == 0; // Returns true on success, false on failure
}
```

*   This function compares the transformed input buffer (`U94y77bvL3HfcnwcAc3UA9MJTvcwjP4j`) with a hardcoded target byte array (`jMunhwoW4bRqeCdJfXvfNrRm`) using `faubPTXHmhV4vfgEpzjqfMRjJ3qunsq9` (equivalent to `strcmp`).
*   If the comparison is successful (returns 0), it prints the deobfuscated success message.
*   Otherwise, it prints the deobfuscated failure message.

### 3. Reversing the Transformation

To find the flag, we need to find the original input (`aixxj3qmUvFTqgqLodmuaEap`) that, when transformed by `wKtyPoT4WdyrkVzhvYUfvqo3M9iPVMd3`, results in a byte sequence identical to `jMunhwoW4bRqeCdJfXvfNrRm`.

**a) Identifying the Target Bytes**

We need the byte values stored in `jMunhwoW4bRqeCdJfXvfNrRm`. Locating this variable in Ghidra's Listing or Memory View revealed the following byte sequence (displayed by Ghidra as signed bytes):

```
{ 45, 56, -65, 50, -16, 5, -88, -75, 4, -101, -116, 83, -54, -25, -16, 103, -10, 89, -60, -15, 80, -25, 122, -91, 116, -85, -36, -39, 80, -9, 90, -67, -74, 43, -98, 49, -112, 55, 8, 29, 62, -87, 44, 105, 10, 103, 56, -97, 14, 43, 36, -109, 114, 31, 64, 109, -44, 123, -18, 81, 26, 79, -54, 109, -20, -15, 36, -53, 114, 5, -15, ... (padding) }
```

For calculations, these need to be treated as unsigned bytes (0-255).

**b) Determining the Flag Length**

The transformation function processes the input including its null terminator. If the original flag has length `L`, the transformation loop runs for `i` from 0 to `L`. The comparison function (`strcmp`) will compare bytes until it finds a mismatch or hits a null byte in *either* string. For a successful match, the transformed input must match the target array exactly up to the transformed null byte, and the byte *after* that in the target array must *also* match the transformed null byte.

Let `output` be the transformed buffer and `target` be `jMunhwoW4bRqeCdJfXvfNrRm`.
We know `output[L] = ((L * 3 + 0x1f) ^ ROL(input[L], 3)) & 0xFF`.
Since `input[L]` is the null terminator (`\0`), `ROL(0, 3)` is 0.
Therefore, `output[L] = (L * 3 + 0x1f) & 0xFF`.

For the check to succeed, we must have `output[i] == target[i]` for `i` from 0 to `L`. This implies that `target[L]` must be equal to the calculated `(L * 3 + 0x1f) & 0xFF`. We can iterate through possible lengths `L` and check this condition against the known `target` bytes to find the correct length.

**c) Deriving the Inverse Transformation**

We need to reverse this equation to find `input[i]`:
`output[i] = ((i * 3 + 0x1f) ^ ROL(input[i], 3)) & 0xFF`

Using the property that `A ^ B = C` implies `A ^ C = B`:
`ROL(input[i], 3) = (output[i] ^ (i * 3 + 0x1f)) & 0xFF`

The inverse operation of Rotate Left (ROL) by 3 bits is **Rotate Right (ROR)** by 3 bits.
`input[i] = ROR( (output[i] ^ (i * 3 + 0x1f)) & 0xFF, 3 )`

### 4. Solution Script (Python)

We can now write a script to perform the length detection and inverse transformation:

```python
import sys

def ror(byte, count):
  """Performs a Rotate Right operation on an 8-bit byte."""
  count %= 8
  return ((byte >> count) | (byte << (8 - count))) & 0xFF

# Target bytes from Ghidra (signed)
signed_bytes = [
    45, 56, -65, 50, -16, 5, -88, -75, 4, -101,
    -116, 83, -54, -25, -16, 103, -10, 89, -60, -15,
    80, -25, 122, -91, 116, -85, -36, -39, 80, -9,
    90, -67, -74, 43, -98, 49, -112, 55, 8, 29,
    62, -87, 44, 105, 10, 103, 56, -97, 14, 43,
    36, -109, 114, 31, 64, 109, -44, 123, -18, 81,
    26, 79, -54, 109, -20, -15, 36, -53, 114, 5,
    -15 # Byte at index 70, used for length check
]

# Convert to unsigned bytes (0-255)
target_bytes = [(b + 256) & 0xFF for b in signed_bytes]

# --- Determine the actual flag length ---
flag_length = -1
# Iterate checking potential lengths against the transformed null terminator value
for L in range(len(target_bytes)):
    expected_transformed_null = (L * 3 + 0x1f) & 0xFF
    if target_bytes[L] == expected_transformed_null:
        flag_length = L
        print(f"[+] Detected flag length: {flag_length}")
        break # Found the length

if flag_length == -1:
    print("[-] Error: Could not determine flag length.")
    sys.exit(1)

# --- Reverse the transformation for indices 0 to L-1 ---
flag = ""
for i in range(flag_length): # Only iterate up to length - 1
    output_byte = target_bytes[i]
    xor_key = (i * 3 + 0x1f) & 0xFF # Calculate the index-dependent XOR key

    # Reverse the XOR
    rotated_input_byte = output_byte ^ xor_key

    # Reverse the ROL(3) by doing ROR(3)
    original_input_byte = ror(rotated_input_byte, 3)

    flag += chr(original_input_byte)

print("\n[*] Flag:", flag)

# Optional: Verify the transformed null terminator calculation
calculated_transformed_null = (flag_length * 3 + 0x1f) & 0xFF
print(f"\n[+] Verification:")
print(f"    Target byte at index {flag_length}: {target_bytes[flag_length]}")
print(f"    Calculated transformed null for length {flag_length}: {calculated_transformed_null}")
if target_bytes[flag_length] == calculated_transformed_null:
    print("    Verification successful.")
else:
    print("    Verification FAILED.")
```

### 5. Result

Running the Python script performs the length check (finding L=70) and then applies the inverse transformation to the first 70 bytes of the target array, yielding the flag:

```
[+] Detected flag length: 70

[*] Flag: FCSC{e30f46b147e7a25a7c8b865d0d895c7c7315f69582f432e9405b6d093b6fb8d3}

[+] Verification:
    Target byte at index 70: 241
    Calculated transformed null for length 70: 241
    Verification successful.
```


## Flag

```
FCSC{e30f46b147e7a25a7c8b865d0d895c7c7315f69582f432e9405b6d093b6fb8d3}
```


### 6. Conclusion

This challenge involved reversing a custom transformation algorithm applied to user input. The key steps were:

1.  Decompiling the binary with Ghidra.
2.  Analyzing the `main` function to understand the program flow (input -> transform -> check).
3.  Dissecting the transformation function to identify the exact algorithm (XOR combined with a bit rotation).
4.  Extracting the target byte array the transformed input is compared against.
5.  Using the way the null terminator was processed to determine the correct length of the flag.
6.  Mathematically deriving the inverse transformation.
7.  Implementing the inverse transformation in a script to recover the original flag from the target bytes.

---