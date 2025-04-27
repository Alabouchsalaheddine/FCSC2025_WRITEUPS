
# Touillette


## Challenge Statement

> I put a stirrer in my flag and... stirred it.
> 
> Reconstruct it!
> 
> Files provided:
> - `output.txt`
> - `touillette.py`

---

## Solution

The `output.txt` contained the following scrambled string:

```
Z2yFm7bCjR6SMWOCSiw{wqKWoJxTtxP4Hf74mQZ4qmghcu1mdX9HND7u8oxF}JsR
```

In the `touillette.py` script, the transformation process hinted that the string was separated into two halves and then merged in a specific way.

We wrote the following script to reverse the transformation:

```python
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
```

By executing this script, we successfully reconstructed the original flag.

---

## Flag

```
FCSC{WT444hmHuFRyb6OwKxP7Zg197xs27RWiqJxfQmuXDoJZmjMSwotHmqcdN8}
```
