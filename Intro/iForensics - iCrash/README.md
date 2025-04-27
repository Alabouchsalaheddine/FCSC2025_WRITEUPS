# iForensics - iCrash


## Challenge Statement

As you pass through customs, the customs officer asks you to hand over your phone and its unlock code. The phone is returned to you a few hours later...

Suspicious, you send your phone to ANSSI's CERT-FR for analysis. CERT-FR analysts carry out a collection on the phone, consisting of a sysdiagnose and a backup.

Note: with the exception of iForensics - iBackdoor 2/2, which depends on the resolution of iForensics - iBackdoor 1/2, the challenges are independent. However, we advise you to work through them in increasing order of difficulty, ending with iForensics - iCompromise..

It seems that a flag has hidden itself in the place where crashes are stored on the phone...

---

## Solution

1. **Unzip the files:**  
   We started by extracting the files from the `backup.tar.xz` and `sysdiagnose_and_crashes.tar.xz` archives.

2. **Explore the folder structure:**  
   After unzipping, open the folder containing the two extracted directories in a code editor, such as VSCode.

3. **Search for the flag:**  
   We searched for the string `FCSC` across the files in the extracted directories. This led us to a file that contained the flag.

4. **The flag location:**  
   The file containing the flag was located at:
   
   ```
   ./private/var/mobile/Library/Logs/CrashReporter/fcsc_intro.txt
   ```

5. **The flag:**  
   The flag in the file is:
   
   ```
   FCSC{7a1ca2d4f17d4e1aa8936f2e906f0be8}
   ```

---

## Flag

```
FCSC{7a1ca2d4f17d4e1aa8936f2e906f0be8}
```
