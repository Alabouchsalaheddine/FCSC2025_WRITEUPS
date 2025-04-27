printed_output = "Z2yFm7bCjR6SMWOCSiw{wqKWoJxTtxP4Hf74mQZ4qmghcu1mdX9HND7u8oxF}JsR"

def reverse_transformation(printed_output):
    half = len(printed_output) // 2
    odd = printed_output[:half]
    even = printed_output[half:]
    x = ''.join(e + o for e, o in zip(even, odd))

    flag_chars = [''] * 64
    for i in range(8):
        for j in range(8):
            flag_index = i + (7 - j) * 8
            flag_chars[flag_index] = x[i * 8 + j]
    return ''.join(flag_chars)

original_flag = reverse_transformation(printed_output)
print(original_flag)