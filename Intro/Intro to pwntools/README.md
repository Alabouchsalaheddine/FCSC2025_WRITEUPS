# Intro to pwntools


## Challenge Statement

> This is not a real challenge, but rather an example of how to use Python to communicate with the remote services of FCSC, Hackropole, and more generally, with any service exposing a TCP port.
> 
> If you are not familiar with these concepts, start by installing the Python package pwntools on your machine. This package is extremely useful in CTFs and helps simplify a lot of tasks.
> 
> In our case, we will only use it to communicate with a service exposing a TCP port.
> 
> This service is accessible here:
> ```
> nc chall.fcsc.fr 2053
> ```
> 
> The port is TCP port number 2053.  
> The server is located at the address chall.fcsc.fr.  
> nc (netcat) is a utility that allows you to connect to a TCP port.  
> Although it is possible to solve this challenge manually or directly from the provided `template.py` file, we recommend studying the different functions used in `template.py`. These are the main functions used in pwntools for communicating with remote services, and they might be useful for you for other FCSC or Hackropole challenges.

---

## Solution

We connected to the service using:

```bash
nc chall.fcsc.fr 2053
```

The interaction began with the following prompt:

```
Welcome to this introduction to pwntools!
First, send me 'Go!' after the '>>>'
>>> Go!
Good! Let's continue!
```

After sending `Go!`, we were prompted to read lines until the `===` marker appeared. Once it did, we were given a number (`7898`), and instructed to add `9` to it, then send the result back:

```
Here is a number: 7898
>>> 7907
Well done!!
```

After sending the correct result (`7907`), the flag was revealed:

---

## Flag

```
FCSC{5bdcc7d8671457aa9366753d9f4cf2ed67832784c383c502f5c3d07361b16158}
```
