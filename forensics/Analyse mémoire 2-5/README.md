
# Analyse mémoire 1/5 - Exfiltration


## Challenge Statement

This challenge is the second part of a 5-part memory analysis series:

- Analyse mémoire 1/5 - Exfiltration ⭐ (dynamic scoring)
- Analyse mémoire 2/5 - Origine de la menace ⭐ (static scoring, 100 points)
- Analyse mémoire 3/5 - Où est le pansement ? ⭐⭐⭐ (dynamic scoring)
- Analyse mémoire 4/5 - Un échelon de plus dans la chaîne ⭐⭐⭐ (dynamic scoring)
- Analyse mémoire 5/5 - Le commencement ⭐⭐ (dynamic scoring)

---

An active malware is confirmed to be running on the machine.  
Now, you must determine **how the attacker managed to execute the malware in memory**.

**Objective**:  
Identify the process that enabled the malware to execute:

- The name of the responsible process
- Its process ID (PID)

---

## Expected Flag Format

```
FCSC{<process_name>:<process_id>}
```

Where:
- `<process_name>` is the name of the process that launched the malware,
- `<process_id>` is its Process ID.

**Example**:

```
FCSC{malware.exe:42}
```

---

**Warning**: You only have 10 submission attempts.

---

## Provided Files

- Memory dump archive (same as previous challenge)

---

## Solution

### Analysis Process

In this challenge, the goal was to identify a suspicious process by analyzing a memory dump. The process `rundll32.exe` was flagged as potentially malicious, and the task was to trace its origin and link it to the responsible parent process.

### Steps Taken

1. **Memory Dump Analysis**:  
   We started by analyzing the memory dump file (`analyse-memoire.dmp`) using Volatility. The command below was run to gather process information:
   ```bash
   vol -f analyse-memoire.dmp windows.pstree
   ```

   This command provides a process tree of all active processes at the time the memory dump was captured.

2. **Identifying Suspicious Process**:  
   From the process tree, we identified `rundll32.exe` as the suspicious process. This process is commonly used by malware for executing dynamic link libraries (DLLs) and can be a sign of malicious activity.

3. **Tracing the Parent Process**:  
   To investigate further, we needed to determine which process had launched `rundll32.exe`. By tracing its parent process, we found that `rundll32.exe` was executed by `svchost.exe`.

   Here is the relevant portion of the process tree:
   ```
   936  800   svchost.exe  0xa50a26148240  10  -  0  False  2025-04-01 22:10:44.000000 UTC  N/A  \Device\HarddiskVolume3\Windows\System32\svchost.exe  C:\Windows\system32\svchost.exe -k DcomLaunch -p C:\Windows\system32\svchost.exe
   *** 1800  936   rundll32.exe  0xa50a270b9200  4  -  0  False  2025-04-01 22:10:45.000000 UTC  N/A  \Device\HarddiskVolume3\Windows\System32\rundll32.exe  rundll32.exe  C:\Windows\system32\rundll32.exe
   ```

4. **Conclusion**:  
   The flag is identified based on the parent-child relationship between the processes:
   ```
   FCSC{svchost.exe:936}
   ```

### Summary

- The suspicious process `rundll32.exe` was traced back to its parent process `svchost.exe` with process ID `936`.
- The flag for this challenge is `FCSC{svchost.exe:936}`.

---

## Flag

```
FCSC{svchost.exe:936}
```