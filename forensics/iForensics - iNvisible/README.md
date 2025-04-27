# iForensics - iNvisible


## Challenge Statement

As you pass through customs, the officer asks for your phone and unlock code.  
When the phone is returned hours later, you feel suspicious and send it to ANSSI's CERT-FR for analysis.  
The analysts collect two artifacts:

- A sysdiagnose
- A full backup

> ⚠️ Note: Except for iForensics - iBackdoor 2/2 (which depends on 1/2), the challenges are independent.  
> It is recommended to solve them in increasing difficulty, ending with iForensics - iCompromise.

---

**Objective**:  
It seems a message could not be sent.  
Find the **recipient** of this unsent message.

---

## Expected Flag Format

```
FCSC{<recipient>}
```

**Example**:

```
FCSC{example@example.com}
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
- Search across all extracted files for email addresses using `grep`:

```bash
grep -aEor '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```

- This command lists many email addresses, some valid, some junk (like image file names with `@2x` etc.).

To filter the real addresses faster, you can prompt an LLM like **Gemini 2.5 Pro Flash** to parse the grep results.

---

**Gemini output (filtered real emails):**

- example@example.com
- robertswigert@icloud.com
- kristy.friedman@outlook.com
- appleid@id.apple.com
- appleid@apple.com
- shj-rsv@princehotels.co.jp

After checking the context, the correct recipient is:

---

## Flag

```
FCSC{kristy.friedman@outlook.com}
```
