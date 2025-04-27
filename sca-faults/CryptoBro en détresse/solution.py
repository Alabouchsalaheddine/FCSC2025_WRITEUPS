import numpy as np
import glob
import os
import sys
from tqdm import tqdm # For progress bars

# Directory containing the trace files
trace_dir = 'traces' # Assuming the script is run in the same directory as the traces

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