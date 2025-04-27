# iForensics - iDevice


## Challenge Statement

As you pass through customs, the officer asks for your phone and unlock code.  
When the phone is returned hours later, you feel suspicious and send it to ANSSI's CERT-FR for analysis.  
The analysts collect two artifacts:

- A sysdiagnose
- A full backup

> ⚠️ Note: Apart from iForensics - iBackdoor 2/2 (which depends on 1/2), the challenges are independent.  
> It is recommended to solve them in increasing difficulty, ending with iForensics - iCompromise.

---

**Objective**:  
Retrieve two pieces of information from the phone:

- **Model Identifier** (e.g., iPhone15,3)
- **iOS Build Number** (e.g., 22E240)

---

## Expected Flag Format

```
FCSC{<model identifier>|<build number>}
```

**Example**:

```
FCSC{iPhone15,3|22E240}
```

---

**Warning**: You only have 5 submission attempts.

---

## Provided Files

- `backup.tar.xz`
- `sysdiagnose_and_crashes.tar.xz`

---

## Solution

- Extract the provided archives.
- Open the extracted folders in a code editor like VSCode.
- Perform a simple text search for key terms like `iPhone`, `build`, or `iOS`.
- The information can be found in the crash logs.

In particular, you can find the flag in the file:

```
iForensics - iCrash/private/var/mobile/Library/Logs/CrashReporter/SiriSearchFeedback-2025-04-07-064530.ips
```

---

## Flag

```
FCSC{iPhone12,3|20A362}
```
