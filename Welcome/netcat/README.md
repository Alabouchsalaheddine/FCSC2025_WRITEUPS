

# Netcat


## Challenge Statement

> Connect to the remote service with the command netcat (nc(1)) given below to grab the flag.
> 
> ```
> nc chall.fcsc.fr 2058
> ```

---

## Solution

This challenge is straightforward: we simply need to connect to the given server using `netcat` from a terminal.

Command to run:
```bash
nc chall.fcsc.fr 2058
```

Upon connecting, the server immediately sends the flag.

---

## Flag

```
FCSC{Tous_les_flags_ressemblent_à_ce_genre_de_chaines_de_caractères!}
```


