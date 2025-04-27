# Analyse mémoire - Pour commencer (2/2)

**Points**: 25  
**Category**: Forensics

---

## Challenge Statement

The memory dump was taken while a user was working on a highly sensitive document. If the workstation was compromised, this document may have been stolen. Can you find:

- The name of the document editing software.
- The name of the document.

The flag is in the format:  
`FCSC{<software name>:<document name>}`

Where:
- `<software name>` is the name of the editing software’s executable.
- `<document name>` is the name of the document being edited by the user (without the file path).

For example:  
`FCSC{calc.exe:My accounts 2025.txt}`

Warning: For this challenge, you only have 10 submission attempts.

---

## Flag

```
FCSC{soffice.exe:[SECRET-SF][TLP-RED]Plan FCSC 2026.odt}
```
