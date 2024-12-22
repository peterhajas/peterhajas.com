# peterhajas.com - The Next Generation

## Notes

This repository hosts the files and scripts for `peterhajas.com`.

## Setup

1. Install Debian Linux
2. `ssh` into it
3. Update packages
4. Install `sudo`
5. Add `phajas` to `sudoers`:
```
echo "phajas ALL=(ALL:ALL) ALL" >> /etc/sudoers
```
6. Add your public key to `~/.ssh/authorized_keys`
7. Run `./password && ansible-playbook playbooks/main.yml --ask-become-pass` and enjoy
8. Make sure expected repos exist and are configured right

## Wiki Notes

Much of this site (maybe, soon, *the whole site*) is powered by TiddlyWiki. This is all in the TiddlyWiki Dockerfile in this repo, which utilizes some scripts.

This all works on a `git` receive of my TiddlyWiki:

* grab all Public-y tiddlers, and export them
* strip the Public tag out of them
* take Public-y tiddlers and do field substitutions if they have a `public_` field in them. For example, `public_title` becomes `title`. This makes it easy to set properties, like title / UI visibility / saver filter / whatever all in pure TiddlyWiki
* import the massaged public tiddlers into a new "base" wiki (just an empty tiddlywiki)
* grab all external attachments that are tagged `Public` and migrate them to /wiki/
* place that at /wiki/index.html in the resulting site
* export an RSS feed of the TiddlyWiki to the same /wiki/
* export static variants of all tiddlers to the same /wiki/

