# iForensics - iWiFi

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
Find the following information:
- SSID of the WiFi network the phone is connected to
- BSSID of the WiFi network
- iCloud account associated with the phone

---

## Expected Flag Format

```
FCSC{<SSID>|<BSSID>|<iCloud account>}
```

**Example**:

```
FCSC{example|00:11:22:33:44:55|example@example.com}
```

---

**Warning**: You only have 5 submission attempts.

---

## Provided Files

- `backup.tar.xz`
- `sysdiagnose_and_crashes.tar.xz`

---

## Solution

1. **Extract all archives**:

```bash
tar -xf backup.tar.xz
```

Then recursively extract nested archives (`.tar.xz`, `.tgz`, etc.):

```bash
find . -type f \( -name "*.tar.xz" -o -name "*.tgz" \) -exec sh -c '
  for archive; do
    dir=$(dirname "$archive")
    case "$archive" in
      *.tar.xz) tar -xf "$archive" -C "$dir" ;;
      *.tgz) tar -xzf "$archive" -C "$dir" ;;
    esac
  done
' sh {} +
```

2. **Find the WiFi information**:
- Search for BSSID (MAC addresses format) using this regex in VSCode:

```regex
([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}
```

- Result found:
  - `ssid='FCSC'`
  - `Bssid: 66:20:95:6C:9B:37`

3. **Find the iCloud account**:
- Search for email addresses in all files (even binary):

```bash
grep -aEor '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```

- Result:
  - `robertswigert@icloud.com`

---

## Final Flag

```
FCSC{FCSC|66:20:95:6C:9B:37|robertswigert@icloud.com}
```
