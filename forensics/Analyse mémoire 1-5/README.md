
# Analyse mémoire 1/5 - Exfiltration


## Challenge Statement

This challenge is the first part of a 5-part memory analysis series:

- Analyse mémoire 1/5 - Exfiltration ⭐ (dynamic scoring)
- Analyse mémoire 2/5 - Origine de la menace ⭐ (static scoring, 100 points)
- Analyse mémoire 3/5 - Où est le pansement ? ⭐⭐⭐ (dynamic scoring)
- Analyse mémoire 4/5 - Un échelon de plus dans la chaîne ⭐⭐⭐ (dynamic scoring)
- Analyse mémoire 5/5 - Le commencement ⭐⭐ (dynamic scoring)

---

An FCSC agent booted their machine to brainstorm challenge ideas for next year. However, during startup, a strange red screen appeared briefly before the system booted normally.

Although they were able to work without issues, a memory dump was collected with the DumpIt tool to investigate potential malware activity.

**Objective**:  
Analyze the memory and identify the malware trying to exfiltrate a document:

- The process running the malware
- The address and port of the attacker's server

---

## Expected Flag Format

```
FCSC{<process_name>:<process_id>:<remote_ip_address>:<remote_port>:<protocol_used>}
```

Where:
- `<process_name>` is the name of the malware process,
- `<process_id>` is its Process ID (PID),
- `<remote_ip_address>` is the IP address of the attacker's server,
- `<remote_port>` is the port on the attacker's server,
- `<protocol_used>` is either `TCP` or `UDP`.

**Example**:

```
FCSC{malware.exe:512:51.255.68.182:21:UDP}
```

---

**Warning**: You only have 10 submission attempts.

---

## Provided Files

- `analyse-memoire.tar.xz` (memory dump archive)

---

## Solution

### 1. Process Inspection with `windows.pslist`

Standard Windows processes were found (e.g., `explorer.exe`, `svchost.exe`, `lsass.exe`, etc.), as well as VirtualBox-related processes (`VBoxService.exe`, `VBoxTray.exe`) and user applications like `LibreOffice`, `Edge`, and `Skype`.

However, **`rundll32.exe`** appeared suspicious:
- While it's a legitimate Windows utility, it's often exploited to execute malicious DLLs stealthily.
- It stood out as a likely candidate for malware execution.

---

### 2. Network Connection Analysis with `windows.netscan`

We filtered network connections for suspicious or external communications.

Anomalous connection found:
```
Proto: TCPv4
Local Address: 10.0.2.15:49709
Foreign Address: 100.68.20.103:443
State: ESTABLISHED
Process: rundll32.exe
PID: 1800
```

This suggests:
- Active outbound connection from `rundll32.exe`
- Connection to a public IP over port **443** (HTTPS), common in C2 or data exfiltration
- High likelihood of malicious behavior

---

## 🏁 Flag

Extracted components:
- **Process name**: `rundll32.exe`
- **PID**: `1800`
- **Remote IP**: `100.68.20.103`
- **Port**: `443`
- **Protocol**: `TCP`

### ✅ Final Flag:
```
FCSC{rundll32.exe:1800:100.68.20.103:443:TCP}
```

---

## 🧰 Tools Used

- [Volatility 3](https://github.com/volatilityfoundation/volatility3)
- Commands:
  - `vol -f dump.mem windows.pslist`
  - `vol -f dump.mem windows.netscan`

---

## 📌 Conclusion

The memory analysis revealed that the `rundll32.exe` process was responsible for suspicious activity, establishing a connection with a public IP over port 443. This strongly indicates the presence of malware attempting to exfiltrate data, validating the agent’s initial concern.


---

## Flag

```
FCSC{rundll32.exe:1800:100.68.20.103:443:TCP}
```