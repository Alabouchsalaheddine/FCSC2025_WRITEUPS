
# SOCrate 1/6 - Technologie


## Challenge Statement

> On webserver machine, what is the working directory of the web application?
> 
> Flag format: `FCSC{/var/www/***/************/}`
> 
> File provided:
> - `socrate.tar.xz`

---

## Solution

We started by extracting the `socrate.tar.xz` file to inspect its contents.

After extracting the archive, we searched through all files for the string `/var/www/` to locate references to the working directory of the web application.

We found multiple results pointing to the same directory running the web application.

The working directory of the web application was:

```
/var/www/app/banque_paouf
```

---

## Flag

```
FCSC{/var/www/app/banque_paouf}
```
