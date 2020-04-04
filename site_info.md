# About this Site

This is a static webpage served from my web server. The site and its scripts are [stored in `git`](https://github.com/peterhajas/peterhajas.com/). I wrote the static site generator myself.

## Writing

When composing on my Mac, I [write in `vim` and preview in Marked 2](/blog/marked2_vim.html). When writing on iPadOS or iOS, I write in iA Writer. Most content on this page is written in [Markdown](https://daringfireball.net/projects/markdown/).

## Building the Site

This site is built with my own static site generator, written in Python. It’s one script - `build.py` - which generates the site and puts it in an `out` directory (ignored by the site’s `.gitgnore`). This build script uses a few conveniences that I wanted. Rather than a templating system, the site relies on simple `before.html` and `after.html` files that get prepended / appended to each page. This includes the `HEAD` element, header, footer, and other content that every page on the site has.

## Previewing

When I want to see how the site content would look on the page itself, I can run `build.py serve live` to serve the page in “live reloading” mode. This fires up an http server on the local machine, and lets me read the site in a web browser. This uses Python’s great `TCPServer`.

The `serve live` flags also inject [LiveJS](https://livejs.com) into the site when building it. The site is then continuously rebuilt, checking if any of the output files have changed since they were last put on disk. This lets me edit any of the site’s content and see it reflected live in the browser.

I fire off this preview in Terminal on my Mac, or using a-Shell on iPadOS / iOS.

## Deploying

Once the content is ready to go, I’ll do a build of the site with `build.py`. Then, I’ll take the contents of the `out` directory and move them to my web server. The git repo embeds a `deploy` shell script that does this with `rsync` for use on my Mac. On my iPad and phone, I have my web server added as a file provider using Secure ShellFish, so I just drag-and-drop the contents over in Files.

***

This site does not use JavaScript, and is served through HTTP.