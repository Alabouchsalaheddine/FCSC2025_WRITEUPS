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