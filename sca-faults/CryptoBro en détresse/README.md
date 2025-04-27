# CryptoBro en détresse


## Challenge Statement

To recover the PIN of my super-secure cryptocurrency wallet, which contains 0.00000001 BTC, I bought a top-tier oscilloscope for 10,000 euros. But I don't really know what to do with all these traces. Maybe you could give me a hand?

I've acquire one trace for each possible PIN, but to avoid triggering a security mechanism and thus erasing the wallet, I turn off the power after a few microseconds after each attempt.

Note: The cryptobro.tar.xz archive contains files named trace_XXXX.npy, where XXXX corresponds to the PIN used to generate the trace. Once you have recovered the PIN, wrap it between FCSC{} to get the flag. For example, if the PIN were 1234, the flag would be FCSC{1234}.

Warning: For this challenge, you only have 10 attempts. Once you have found the correct technique to use, there will be no ambiguity in finding a unique PIN code.

**Provided file :** cryptobro.tar.xz

---

## Solution


A robust technique often used in such scenarios is **Differential Power Analysis (DPA)**, or a related variant like **Correlation Power Analysis (CPA)**. However, a simpler differential approach might suffice here, directly exploiting the sequential nature of PIN checks combined with the early power cut.

**Improved Hypothesis & Strategy: Differential Analysis Based on Early Exit**

1.  **Sequential Check:** Assume the PIN check works sequentially: check digit 1, if wrong exit; if correct, check digit 2, if wrong exit; etc.
2.  **Early Power Cut:** The power cut happens very early. It's likely happening *during* the check of the first few digits.
3.  **Differential Leakage:**
    *   Consider the first digit. All traces starting with the *correct* first digit will proceed to check the second digit (before the power cut). All traces starting with an *incorrect* first digit will likely take a different path (e.g., prepare to exit) almost immediately.
    *   This difference in execution path should cause a difference in power consumption *after* the point where the first digit is checked.
    *   We can find the correct first digit by comparing the *average* trace of all PINs starting with '0' vs the *average* trace of all PINs starting with '1', and so on. The average trace corresponding to the correct first digit should look different from the other nine average traces.
    *   Once the first digit is known, we repeat the process for the second digit, only considering traces that start with the correct first digit. We compare the average trace of PINs starting with `Correct1`+'0' vs `Correct1`+'1', etc.
    *   We repeat this for all four digits.

**Implementation Steps (Differential Approach):**

1.  **Load Data:** Need a way to efficiently load traces.
2.  **Iterate Digit by Digit:**
    *   **For Digit 1:**
        *   Group traces into 10 sets based on the first digit (0xxx, 1xxx, ..., 9xxx). Each set has 1000 traces.
        *   Calculate the average power trace for each set.
        *   Compare the 10 average traces. The one that stands out (e.g., has the largest difference from the overall average of all traces, or looks visually distinct when plotted) corresponds to the correct first digit. A common way to quantify the difference is to calculate the sum of squared differences between each group's average trace and the average of *all* traces in this step.
    *   **For Digit 2 (assuming Digit 1 is D1):**
        *   Group traces starting with D1 into 10 sets based on the second digit (D10xx, D11xx, ..., D19xx). Each set has 100 traces.
        *   Calculate the average power trace for each set.
        *   Compare these 10 average traces to find the one that stands out. This gives the correct second digit (D2).
    *   **For Digit 3 (assuming Digits 1, 2 are D1, D2):**
        *   Group traces starting with D1D2 into 10 sets based on the third digit (D1D20x, D1D21x, ..., D1D29x). Each set has 10 traces.
        *   Calculate the average trace for each set.
        *   Compare these 10 average traces to find the correct third digit (D3).
    *   **For Digit 4 (assuming Digits 1, 2, 3 are D1, D2, D3):**
        *   Group traces starting with D1D2D3 into 10 sets based on the fourth digit (D1D2D30, D1D2D31, ..., D1D2D39). Each set has 1 trace (so just use the individual traces).
        *   Compare these 10 traces to find the correct fourth digit (D4). Comparing individual traces might be noisy; comparing the average traces from the previous step might already reveal the 4th digit, or comparing these last 10 individual traces against the average of the D1D2Dxxx traces might work. A simpler approach for the last digit might be necessary if comparing single traces is too noisy - perhaps the comparison method needs refinement. Let's stick to the averaging method for consistency first. Average trace for D1D2D30 (1 trace), D1D2D31 (1 trace)... D1D2D39 (1 trace). Compare these 10 "averages" (which are just the individual traces).

**Refined Python Code (Differential Approach)**

```python
import numpy as np
import glob
import os
import sys
from tqdm import tqdm # For progress bars

# Directory containing the trace files
trace_dir = '.' # Assuming the script is run in the same directory as the traces

# Cache for loaded traces to speed up repeated access (optional, depends on memory)
# trace_cache = {}

def format_pin(pin_int):
    """Formats an integer PIN to XXXX string"""
    return f"{pin_int:04d}"

def load_trace(pin_int):
    """Loads a single trace file, returns None if not found"""
    pin_str = format_pin(pin_int)
    trace_file = os.path.join(trace_dir, f"trace_{pin_str}.npy")
    # if pin_str in trace_cache:
    #     return trace_cache[pin_str]
    try:
        trace_data = np.load(trace_file)
        # trace_cache[pin_str] = trace_data
        return trace_data
    except FileNotFoundError:
        # print(f"Warning: Trace file not found for PIN {pin_str}")
        return None
    except Exception as e:
        print(f"Error loading trace for PIN {pin_str}: {e}")
        return None

def get_average_trace(pin_list):
    """Calculates the average trace for a list of PIN integers"""
    traces = []
    for pin_int in pin_list:
        trace = load_trace(pin_int)
        if trace is not None:
            traces.append(trace)
    
    if not traces:
        return None # No valid traces found for this list

    # Ensure all traces have the same length (they should based on the problem description)
    # If not, truncation or padding might be needed, but let's assume consistency first.
    try:
        stacked_traces = np.stack(traces, axis=0)
        average_trace = np.mean(stacked_traces, axis=0)
        return average_trace
    except ValueError as e:
        print(f"Error stacking traces (likely inconsistent lengths): {e}")
        # Basic check: Find min length and truncate?
        min_len = min(len(t) for t in traces)
        truncated_traces = [t[:min_len] for t in traces]
        if not truncated_traces:
             return None
        try:
            stacked_traces = np.stack(truncated_traces, axis=0)
            average_trace = np.mean(stacked_traces, axis=0)
            print(f"Warning: Traces had inconsistent lengths, truncated to {min_len}")
            return average_trace
        except Exception as e2:
             print(f"Failed even after truncation: {e2}")
             return None


# --- Main Differential Analysis Logic ---

known_pin_prefix = ""
num_digits = 4

# Check if trace files exist
all_trace_files = glob.glob(os.path.join(trace_dir, 'trace_*.npy'))
if not all_trace_files:
    print(f"Error: No trace files found in directory '{trace_dir}'.")
    print("Please make sure the trace_*.npy files are in the correct directory.")
    sys.exit(1)
print(f"Found {len(all_trace_files)} trace files. Starting differential analysis...")


for digit_index in range(num_digits):
    print(f"\n--- Analyzing Digit {digit_index + 1} ---")
    
    average_traces = {}
    pin_lists = {} # Store the list of pins for each group

    # 1. Generate PIN lists and calculate average traces for each guess
    for guess_digit in range(10):
        current_guess_prefix = known_pin_prefix + str(guess_digit)
        
        # Generate list of PINs matching the current prefix
        # Example: digit_index=0, guess=1 -> "1" -> 1000-1999
        # Example: digit_index=1, known="1", guess=2 -> "12" -> 1200-1299
        start_pin = int(current_guess_prefix.ljust(num_digits, '0'))
        end_pin = int(current_guess_prefix.ljust(num_digits, '9'))
        
        pin_list = list(range(start_pin, end_pin + 1))
        pin_lists[guess_digit] = pin_list # Store for later calculation if needed

        print(f"Calculating average trace for prefix '{current_guess_prefix}' ({len(pin_list)} traces)...")
        avg_trace = get_average_trace(pin_list)
        
        if avg_trace is None:
            print(f"Error: Could not compute average trace for prefix {current_guess_prefix}")
            # Decide how to handle this - skip digit? Exit? For now, store None.
            average_traces[guess_digit] = None
        else:
            average_traces[guess_digit] = avg_trace

    # Filter out None traces before calculating overall average
    valid_avg_traces = [avg for avg in average_traces.values() if avg is not None]
    if not valid_avg_traces:
        print(f"Error: No valid average traces computed for digit {digit_index + 1}. Cannot proceed.")
        sys.exit(1)
    
    # 2. Calculate the overall average trace for this digit position
    overall_average_trace = np.mean(np.stack(valid_avg_traces, axis=0), axis=0)

    # 3. Find the digit whose average trace differs most from the overall average
    max_diff = -1.0
    best_digit = -1
    
    diff_values = {}

    print("Comparing average traces...")
    for guess_digit in range(10):
        if average_traces[guess_digit] is not None:
            # Calculate difference metric (Sum of Squared Differences)
            diff = np.sum((average_traces[guess_digit] - overall_average_trace)**2)
            diff_values[guess_digit] = diff
            # print(f"  Digit {guess_digit}: Difference = {diff}") # Debugging
            if diff > max_diff:
                max_diff = diff
                best_digit = guess_digit
        else:
            diff_values[guess_digit] = 0 # Or None / NaN

    if best_digit == -1:
        print(f"Error: Could not determine best digit for position {digit_index + 1}.")
        sys.exit(1)
        
    # Print differences for verification
    print("Differences from overall average trace:")
    for g in range(10):
         print(f"  Digit {g}: {diff_values.get(g, 'N/A'):.4f} {'<-- MAX' if g == best_digit else ''}")


    # 4. Append the best digit to our known prefix
    known_pin_prefix += str(best_digit)
    print(f"==> Found Digit {digit_index + 1}: {best_digit}")
    print(f"Current PIN prefix: {known_pin_prefix}")


# --- Final Result ---
if len(known_pin_prefix) == num_digits:
    found_pin = known_pin_prefix
    print(f"\nAnalysis complete.")
    print(f"Recovered PIN: {found_pin}")
    print(f"The flag is: FCSC{{{found_pin}}}")
else:
    print("\nAnalysis failed to recover the full PIN.")

```

**Explanation and Why This is Likely Better:**

1.  **Noise Reduction:** Averaging traces within a group (e.g., all traces starting with '1') significantly reduces random noise, making the underlying signal (power consumption related to computation) clearer.
2.  **Direct Comparison:** We are directly comparing the behavior of the device when processing different candidate digits at a specific position. The correct digit *should* cause a different execution path (proceeding vs. failing early), which averaging should reveal.
3.  **Robustness:** This method is less sensitive to one or two noisy individual traces compared to the "find max energy" approach. The difference metric (sum of squared differences) quantifies how much a group's average behavior deviates from the overall average behavior at that stage.
4.  **Alignment with Clues:** This differential approach is a standard SCA technique and directly uses the implication of the early power cut (differential execution paths). It's designed to find a unique result with high confidence if the leakage exists.

**To Run:**

1.  Save the code as `solve_diff.py`.
2.  Extract `cryptobro.tar.xz` so the `trace_*.npy` files are in the same directory (or adjust `trace_dir`).
3.  Ensure you have `numpy` and `tqdm` installed (`pip install numpy tqdm`).
4.  Run `python solve_diff.py`.

This differential method has a much higher chance of success for this type of challenge setup. It directly targets the expected side-channel leakage resulting from the described scenario.


---

## Flag

```
FCSC{9466}
```
