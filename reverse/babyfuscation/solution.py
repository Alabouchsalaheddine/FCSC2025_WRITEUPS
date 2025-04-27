import sys

def ror(byte, count):
  """Performs a Rotate Right operation on an 8-bit byte."""
  count %= 8
  return ((byte >> count) | (byte << (8 - count))) & 0xFF

# Original signed bytes from Ghidra
signed_bytes = [
    45, 56, -65, 50, -16, 5, -88, -75, 4, -101,
    -116, 83, -54, -25, -16, 103, -10, 89, -60, -15,
    80, -25, 122, -91, 116, -85, -36, -39, 80, -9,
    90, -67, -74, 43, -98, 49, -112, 55, 8, 29,
    62, -87, 44, 105, 10, 103, 56, -97, 14, 43,
    36, -109, 114, 31, 64, 109, -44, 123, -18, 81,
    26, 79, -54, 109, -20, -15, 36, -53, 114, 5,
    -15 # Only up to the 70th byte based on length check below
    # The rest are padding or unused
]

# Convert to unsigned bytes (0-255)
target_bytes = [(b + 256) & 0xFF for b in signed_bytes]

# --- Determine the actual flag length ---
flag_length = -1
for L in range(len(target_bytes)):
    # Calculate what the transformed null terminator should be for length L
    expected_transformed_null = (L * 3 + 0x1f) & 0xFF
    # Check if the byte at index L in the target array matches this value
    if target_bytes[L] == expected_transformed_null:
        flag_length = L
        print(f"Detected flag length: {flag_length}")
        break

if flag_length == -1:
    print("Error: Could not determine flag length based on transformed null terminator.")
    sys.exit(1)

# --- Reverse the transformation for indices 0 to L-1 ---
flag = ""
for i in range(flag_length): # Loop only up to flag_length - 1
    output_byte = target_bytes[i]
    xor_key = (i * 3 + 0x1f) & 0xFF # Calculate the index-dependent XOR part

    # Reverse the XOR
    rotated_input_byte = output_byte ^ xor_key

    # Reverse the ROL(3) by doing ROR(3)
    original_input_byte = ror(rotated_input_byte, 3)

    flag += chr(original_input_byte)

print("Flag:", flag)

# Optional: Verify the transformed null terminator calculation
calculated_transformed_null = (flag_length * 3 + 0x1f) & 0xFF
print(f"Target byte at index {flag_length}: {target_bytes[flag_length]}")
print(f"Calculated transformed null for length {flag_length}: {calculated_transformed_null}")
if target_bytes[flag_length] == calculated_transformed_null:
    print("Verification successful.")
else:
    print("Verification FAILED.")