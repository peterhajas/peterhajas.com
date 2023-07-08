---
title: "Upgrading a Nintendo Switch SD card"
date: 2019-12-21T21:10:00-07:00
emoji: 🎮💾
---

I own a Nintendo Switch console. Because I don't want physical games cluttering my home, I get all my games digitally. I recently started running out of room and needed a new SD card to hold my games. This path ended up being circuitous, taking me through fake flash storage, the Switch's file structure, and its operating system's treatment of Unix file attributes.

# A new card

I purchased a Samsung 512GB SD card from Amazon for $65. I'm shocked at how cheap SD cards are now. This replaced my old 128GB card.

Here's the old card:

![The old SD card](/nintendo_oldcard.jpeg)

And here's the new card:

![The new SD card](/nintendo_newcard.jpeg)

Flash memory has never been more popular. Unfortunately, there has been a recent rise of **fake flash** memory. These are USB keys, SD cards, and solid state disks that masquerade as a larger capacity, but will lose your data or fail to read / write properly.

After my new card arrived, I wanted to check its authenticity. Is this a real 512GB SD card? Or a fake?

# The `f3` tool

[`f3`](http://oss.digirati.com.br/f3/) is a tool to verify the authenticity of flash memory. It stands for "Fight Flash Fraud" or "Fight Fake Flash". From the site:

> I started this project when I bought a 32GB microSDHC card for my Android phone back in 2010, and found out that this card always fails when one fills it up.

I installed it on my Mac with `brew install f3`. This installed two binaries: `f3write` and `f3read`.

`f3write` writes contiguous 1GB files to your card until it has exhausted its space. It will also report on the write speed for this operation. You use it by running it on the path you want to write to. It will report progress when running:

    $ f3write /Volumes/test
    F3 write 7.2
    Copyright (C) 2010 Digirati Internet LTDA.
    This is free software; see the source for copying conditions.

    Free space: 476.69 GB
    Creating file 1.h2w ... OK!                           
    Creating file 2.h2w ... OK!                           
    ...
    Creating file 476.h2w ... OK!                        
    Creating file 477.h2w ... OK!                       
    Free space: 1.38 MB
    Average writing speed: 77.17 MB/s

My card got 77MB/s, which comes out to about 2 hours of write time (this is about how long it felt). After doing the write step, you can run `f3read` to verify that the files made it there successfully:

    $ f3read /Volumes/test
    F3 read 7.2
    Copyright (C) 2010 Digirati Internet LTDA.
    This is free software; see the source for copying conditions.

                      SECTORS      ok/corrupted/changed/overwritten
    Validating file 1.h2w ... 2097152/        0/      0/      0
    Validating file 2.h2w ... 2097152/        0/      0/      0
    ...
    Validating file 476.h2w ... 2097152/        0/      0/      0
    Validating file 477.h2w ... 1432983/        0/      0/      0

      Data OK: 476.68 GB (999677335 sectors)
    Data LOST: 0.00 Byte (0 sectors)
               Corrupted: 0.00 Byte (0 sectors)
        Slightly changed: 0.00 Byte (0 sectors)
             Overwritten: 0.00 Byte (0 sectors)
    Average reading speed: 71.12 MB/s

This will read each of the 1GB files created by `f3write`, verifying they did not experience any data loss. This will also report on your card's read speed. Mine was 71MB/s, which also felt like around 2 hours.

Cool, a real SD card that works! Next step: move my games over.

# Switch SD file structure

Plugging my old SD card into my machine, `diskutil` reports an NTFS filesystem:

    $ diskutil list
    /dev/disk3 (external, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:     FDisk_partition_scheme                        *127.9 GB   disk3
       1:               Windows_NTFS                         127.8 GB   disk3s1

The hierarchy on the card (named "Untitled") has a single "Nintendo" folder on it. What's in there?

    $ tree Nintendo
    Nintendo/
    ├── Album
    │   ├── 2017
    │   ├── 2018
    │   └── 2019
    ├── Contents
    │   ├── placehld
    │   ├── private
    │   ├── private1
    │   └── registered
    ├── save
    └── saveMeta

    829 directories, 688 files

(heavily truncated)

So, it looks like:
- `Album`, which includes all my screenshots and video recordings arranged by year
- `Content`, which has some subdirectories:
    - `placehld`, which has some empty directories - likely placeholders given the filename
    - `private`, a 16B file which looks like it contains a key
    - `private1`, a 32B file which looks like it contains a different key
    - `registered`, which appears to contain all the games

I've used the majority of the card's 128GB space:

    $ du -skh /Volumes/Untitled
    111G    /Volumes/Untitled

# Formatting the card

Next step was to insert the 512GB card into the Switch and ask it to format. This process took about 3 seconds, then the console rebooted itself. I verified that the card was now NTFS:

    $ diskutil list
    /dev/disk3 (external, physical):
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:     FDisk_partition_scheme                        *512.1 GB   disk3
       1:               Windows_NTFS                         512.0 GB   disk3s1

# Backing up the card

I don't have two SD card slots on my machine, so I'll need to copy the data first to my computer, then onto the card. We can use `rsync` to do this:

    $ mkdir nintendo_backup
    $ rsync -avz /Volumes/Untitled nintendo_backup/

I used `rsync` in `archive` mode by passing the `-a` flag, which according to `man rsync` will:

> ...ensure that symbolic links, devices, attributes, permissions, ownerships, etc. are preserved...

Perfect! I also passed `-v` for verbose, and `-z` to use compression as the files are moved.

# Restoring to the new card

Now it's time to restore to the new card. After unmounting the smaller card and inserting the new card, it's a simple matter of `rsync`ing the files back:

    rsync -avz nintendo_backup/Untitled/ /Volumes/Untitled

# Trying it out

With the `rsync` step done, we can test out the card:

![The card's not working](/nintendo_error.jpeg)

It doesn't work! The Switch responds with error `2016-0247` and is unable to access the card

I then tried copying the contents of `nintendo_backup` over the `rsync`'d backup files with Finder. Perhaps the `rsync` step missed something? Or my machine fell asleep?

Nope, same error. I tried the original card to verify my Switch was still functional. The original card works fine.

# Debugging the issue

So, we've got a new SD card that the Switch won't see:

- it was formatted by the Switch's software, so any secret partitions or files should be there
- it contains an `rsync` archive copy of the games and media from the original card
- the Switch read the card successfully when formatting it, but hasn't since the restore succeeded

The [Nintendo support site](https://en-americas-support.nintendo.com/app/answers/detail/a_id/27595/) seems to suggest similar steps to those I followed:

> - Open Windows Explorer (for PC) and access the microSD card.
> - Highlight the data and drag it to the desktop.
> - If you are moving your content to a new microSD card, be sure to first format the new card per our recommendations.
> - Once the new card has been formatted, continue with the instructions below.
> - Eject the first microSD card, then insert the second microSD card into the slot or reader/writer.
> - Using Windows Explorer access the microSD card again.
> - Drag the data from the desktop to the new microSD card, then insert the new microSD card into the Nintendo Switch console.

Although it does contain this strange warning:

> Important: This process may not be able to copy the microSD card contents correctly in environments other than Windows (such as Mac).

# A fix

Turns out I was missing the archive attribute on the card. Simply running `sudo chflags -R arch /Volumes/Untitled` to fix up the Archive attribute fixed the issue (I also did a `sudo dot_clean -mn` on the directory). Phew! Look at all that space:

![A screenshot showing the free space on the new larger card](/nintendo_freespace.jpeg)

# Why did this break?

I'm not totally sure. My hunch is that an archive attribute on the files was confusing the Switch's SD card parsing. It looks like the Nintendo Switch's OS is not Unix-derived, but rather an [evolution of the 3DS OS](https://en.wikipedia.org/wiki/Nintendo_Switch_system_software). It's possible that some file attributes from Unix may have confused the Switch.
