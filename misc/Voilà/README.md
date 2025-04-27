# Challenge Name: Voilà


## Statement

Alice loves listening to music. Unfortunately, she misconfigured her firewall and accidentally exposed her music collection on the Internet.

Alice organizes her personal collection in an unconventional way: instead of sorting by genre, album, or artist, she renames her music files based on her imagination.

She assures you that you won't be able to find the real name of the song associated with the file flag.opus. Prove her wrong.

The flag format is: FCSC{Artist_Song}. For example: FCSC{ABBA_Gimme! Gimme! Gimme! (A Man After Midnight)}. The flag is not case-sensitive.

Alice's music collection is accessible at nc chall.fcsc.fr 2052.

---

## Solution


To retrieve the flag from the challenge, I followed these steps:

---

### 1. Connect to the Remote MPD Server

I start by connecting to the challenge server:

```bash
nc chall.fcsc.fr 2052
```

Upon connection, the server responds:

```
OK MPD 0.23.5
```

This confirms we are interacting with an **MPD (Music Player Daemon)**.

---

### 2. List All Available Audio Files

Using the command:

```bash
listallinfo
```

We get the following file listing:

```
file: flag.opus
...
Time: 87
duration: 86.726
```

Among the files listed, `flag.opus` is the one that stands out.  
**Important**: We take note of the file’s **duration** — `87` seconds — as it will be required for querying AcoustID.

---

### 3. Extract the Chromaprint Fingerprint

We extract the audio fingerprint for `flag.opus` using:

```bash
getfingerprint "flag.opus"
```

This returns a **Chromaprint fingerprint**, a compact digital representation of the audio.  
Here is a snippet (truncated for readability):

```
chromaprint: AQACpUrCTIkiSQtSaPgPcMeP69AR5uiPVY6J-EHzQXuOD3llNOeEPkLeQ0dshmhE7ag2RB-ShcoP1zmK0wjfx9ByHvl-PDmmp2juHIeOR8PxJ2geJUfx5Ih5JEeP6pww_TB3BXWyQ2uGoy_-Cs-RI3ly4mhO_IWrNkQfHGMYHnkUJC-ON8L2UMKH58ihIoy0IpTzQ0uDsOtw2E0TPPPwGwnPDPk2PDp--IvxDfsRF8mTEC8e_LoEP8eNC3pwVF-Otwyq_Zh-qXDzCD9-hNB5fMLL4zH6GSLeLIg-EtaP_Bkq6OPxXPgw5ckW1MeTCzr-DN2LalEOPUeeNPh4NJ1S1Gl8_OgZLkiWD_nxyGif5phyxThiJNaBPxb-CH5i40ieID8eVGZRjUsT9FewOdCPoy_-4-nx5Eda5Uh-oO_ht0F7_JiUCdV55EoPHbmEN4KrKEf0QEeMazkcqniOMDeSdcxRG03TFKdzPPDYkTie45pR5h-aB8ePMz3OQ36Ob8Jz9JPw7vBt9MePHw8vVE-CRo6KpD5y9C9wNHjwHM0Rnrih82iP8C9yyXiHGA1vdD9uZXiOz_LQ7GaIHr_wI0_yILlhPseP8_jxJMeP5ugZHj36DvmJ5MUdPCX6TEZz48GFZ9fxHz-qJyes-EEyKcsR_EWfMYV5UujxCz5OPM_w48fTI5QeHnJ15OzgHe2HojmPKx-KB37QI_ka5ClOfMfzo0fzHj-uIfmRFz8e7-gzofnw4NfxXOgV4cf1IGGSEDn6oif8DD3wwHuQJzr0B39wHhce5HCe4r2M5xl-jmh2beh3HJWPfkeeB8kpeFmeHBd-PHzw5PjRh0dz4sQtBcmPPMXT4GZ2NLfQL_jxC7-O48-DJz0RJmKOZMevoD-FZg-eK8MP_zh-PE9wRvhxpT7CD7qQLx28oAuPw-eBdl9w_PDR43iD_Die4zkk3R3-HEf_Bc0P7TnyC33A3cIeBX3QXBfyFPKSoC_-FOlJCn2e4sY-1Oki-EVSZImOj8OZB--DPjr8oz3yQQdH7XhyfDF6-NDxB_l-RP1R9Rm0oN6RH9fQh4oxpbrwI2-hPkQ47ziFsLoCnemRn3jgL81xWsGPhM-iIA8eNGfRP9iHGIk1nLgvPHoS-MHxCPqc4-hZnCxOJ8HWHnpynOiLX3iQH8mV4-hhRm3gaurR4-Fx6sgXJA8u9NvRdIoPPsihHmTx5dCT_cjjDBfsGhfTxHiQ8MyQb8MjHL6PPcKRdMiP484j9D2a57jxIXkSxEdXDtWZYyp3-BK-MyKOGz3yA-pxfA90NA8idSSO_0SoMkfzQw9y9JlyNK0X5MeP5DyqPMOWZceTI_2hnQibo2kaPHKCB34f5A6RPDhaLseUZyrwQ92GHx_uR2geJQ96HHmC5A8qs8GHD-aeYPqDOoHK4hx6_BWOZ3iC5AhTB31o_PAZDxcP7NuHH0Hy40dTfUdHGhczBMl__PhnoenY4DiOZEd-_PiP6cd29MGPEzfyQ4PxQ8d1pD3GwseOHzH0I1eG4zQuHMifQwdiPjgMBMJ_5PiO7cARHPrx48fhHzpyHDd8HI8iAi-eDsla5Acf42tx5fjxU-hHnDn-I25ySFeSiFMAA5xETBEshZBeMEMRhQZDKwxzAgBhADJCISARoIACgIDRCihgCEXAAMaIQ8AIBBAh5RqECDzAMeSAQdQAwYQUAgQAkMCIMGMEAIQwZBwTFAFAiQICGCUQQ-AgJFgwxBIEjQNMCWEMAkAwAogjCBFlNQJIGASAAQQJw6AQBjApASCGeCsIERYpwhggD1kCFHJMAYGEAIABxRAiCgwCCRCMCGRJQ1wQJwQBCgPDKENGUICYYoIx4IgjhAINHBLESAgEAEp7TwQghDkKiLEMKYAZVKARxjggAAjHhBMKMGcYkyZQwAwFBDruJAEkQKU9YYAgAQ2QCgvEmVAGAUmYYCAdYRgygEFiCRGOAAG4BQQBDpwigEQABAACUVAYMQhYIIgw1jLBgCSIGWVcM4xwwgAQjCE3jHFUKQauNKYwAREwjAsADAHCCKOFIMQCBASSAhjAgAICImOZAkg5TSUyRAABECWQK6GwMRAQJAhAAjAqgDGCEMOAYQAxRAwThhEiDAIQaEOYUgQEBiARoQEBNAnAAEAQIsEgo4DBAFNghDCCIeKQABQBhTwBIiRiIBoEOMGEWAAhZJAjAmEjBGAeAEYQAxIJwgACwDFDiHUGESOB4UARQB0wQAjABWROCKQQMBIACYwCYiFABQJIKQyEFE5x4YDV0hgGwAMVCCIVCIB5ZKiARDkDpBlKGlUqAApSJBwyhhvAGEFIAAA
```

---

### 4. Query AcoustID API

We use the [AcoustID Web Service](https://acoustid.org/webservice) to identify the audio file:

- **API Endpoint**:
  ```
  https://api.acoustid.org/v2/lookup
  ```

- **Query Parameters**:
  - `client`: HdifjIZKIAA (provided test API key)
  - `meta`: recordings+releasegroups+compress
  - `duration`: `87` (must match the duration of the audio file from MPD)
  - `fingerprint`: <Chromaprint fingerprint>

- **Example API Request**:

```bash
curl "https://api.acoustid.org/v2/lookup?client=HdifjIZKIAA&meta=recordings+releasegroups+compress&duration=87&fingerprint=AQACpUrCTIkiSQtSaPgPcMeP69AR5uiPVY6J-EHzQXuOD3llNOeEPkLeQ0dshmhE7ag2RB-ShcoP1zmK0wjfx9ByHvl-PDmmp2juHIeOR8PxJ2geJUfx5Ih5JEeP6pww_TB3BXWyQ2uGoy_-Cs-RI3ly4mhO_IWrNkQfHGMYHnkUJC-ON8L2UMKH58ihIoy0IpTzQ0uDsOtw2E0TPPPwGwnPDPk2PDp--IvxDfsRF8mTEC8e_LoEP8eNC3pwVF-Otwyq_Zh-qXDzCD9-hNB5fMLL4zH6GSLeLIg-EtaP_Bkq6OPxXPgw5ckW1MeTCzr-DN2LalEOPUeeNPh4NJ1S1Gl8_OgZLkiWD_nxyGif5phyxThiJNaBPxb-CH5i40ieID8eVGZRjUsT9FewOdCPoy_-4-nx5Eda5Uh-oO_ht0F7_JiUCdV55EoPHbmEN4KrKEf0QEeMazkcqniOMDeSdcxRG03TFKdzPPDYkTie45pR5h-aB8ePMz3OQ36Ob8Jz9JPw7vBt9MePHw8vVE-CRo6KpD5y9C9wNHjwHM0Rnrih82iP8C9yyXiHGA1vdD9uZXiOz_LQ7GaIHr_wI0_yILlhPseP8_jxJMeP5ugZHj36DvmJ5MUdPCX6TEZz48GFZ9fxHz-qJyes-EEyKcsR_EWfMYV5UujxCz5OPM_w48fTI5QeHnJ15OzgHe2HojmPKx-KB37QI_ka5ClOfMfzo0fzHj-uIfmRFz8e7-gzofnw4NfxXOgV4cf1IGGSEDn6oif8DD3wwHuQJzr0B39wHhce5HCe4r2M5xl-jmh2beh3HJWPfkeeB8kpeFmeHBd-PHzw5PjRh0dz4sQtBcmPPMXT4GZ2NLfQL_jxC7-O48-DJz0RJmKOZMevoD-FZg-eK8MP_zh-PE9wRvhxpT7CD7qQLx28oAuPw-eBdl9w_PDR43iD_Die4zkk3R3-HEf_Bc0P7TnyC33A3cIeBX3QXBfyFPKSoC_-FOlJCn2e4sY-1Oki-EVSZImOj8OZB--DPjr8oz3yQQdH7XhyfDF6-NDxB_l-RP1R9Rm0oN6RH9fQh4oxpbrwI2-hPkQ47ziFsLoCnemRn3jgL81xWsGPhM-iIA8eNGfRP9iHGIk1nLgvPHoS-MHxCPqc4-hZnCxOJ8HWHnpynOiLX3iQH8mV4-hhRm3gaurR4-Fx6sgXJA8u9NvRdIoPPsihHmTx5dCT_cjjDBfsGhfTxHiQ8MyQb8MjHL6PPcKRdMiP484j9D2a57jxIXkSxEdXDtWZYyp3-BK-MyKOGz3yA-pxfA90NA8idSSO_0SoMkfzQw9y9JlyNK0X5MeP5DyqPMOWZceTI_2hnQibo2kaPHKCB34f5A6RPDhaLseUZyrwQ92GHx_uR2geJQ96HHmC5A8qs8GHD-aeYPqDOoHK4hx6_BWOZ3iC5AhTB31o_PAZDxcP7NuHH0Hy40dTfUdHGhczBMl__PhnoenY4DiOZEd-_PiP6cd29MGPEzfyQ4PxQ8d1pD3GwseOHzH0I1eG4zQuHMifQwdiPjgMBMJ_5PiO7cARHPrx48fhHzpyHDd8HI8iAi-eDsla5Acf42tx5fjxU-hHnDn-I25ySFeSiFMAA5xETBEshZBeMEMRhQZDKwxzAgBhADJCISARoIACgIDRCihgCEXAAMaIQ8AIBBAh5RqECDzAMeSAQdQAwYQUAgQAkMCIMGMEAIQwZBwTFAFAiQICGCUQQ-AgJFgwxBIEjQNMCWEMAkAwAogjCBFlNQJIGASAAQQJw6AQBjApASCGeCsIERYpwhggD1kCFHJMAYGEAIABxRAiCgwCCRCMCGRJQ1wQJwQBCgPDKENGUICYYoIx4IgjhAINHBLESAgEAEp7TwQghDkKiLEMKYAZVKARxjggAAjHhBMKMGcYkyZQwAwFBDruJAEkQKU9YYAgAQ2QCgvEmVAGAUmYYCAdYRgygEFiCRGOAAG4BQQBDpwigEQABAACUVAYMQhYIIgw1jLBgCSIGWVcM4xwwgAQjCE3jHFUKQauNKYwAREwjAsADAHCCKOFIMQCBASSAhjAgAICImOZAkg5TSUyRAABECWQK6GwMRAQJAhAAjAqgDGCEMOAYQAxRAwThhEiDAIQaEOYUgQEBiARoQEBNAnAAEAQIsEgo4DBAFNghDCCIeKQABQBhTwBIiRiIBoEOMGEWAAhZJAjAmEjBGAeAEYQAxIJwgACwDFDiHUGESOB4UARQB0wQAjABWROCKQQMBIACYwCYiFABQJIKQyEFE5x4YDV0hgGwAMVCCIVCIB5ZKiARDkDpBlKGlUqAApSJBwyhhvAGEFIAAA"
```

⚠️ **Note**: Using the correct duration (`87` seconds) is essential to get accurate results from the API.

---

### 5. Parse the API Response

The API returns a JSON object identifying the audio:

```json
{
  "results": [
    {
      "recordings": [
        {
          "artists": [{"name": "Aya Higuchi"}],
          "title": "Wiosna"
        }
      ]
    }
  ],
  "status": "ok"
}
```

---

### 6. Construct the Flag

According to the challenge format:

```
FCSC{Artist_Title}
```

The correct flag is:

```
FCSC{Aya Higuchi_Wiosna}
```


---

## Flag

```
FCSC{Aya Higuchi_Wiosna}
```
