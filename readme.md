# peterhajas.com

This repository hosts the content powering [peterhajas.com](http://peterhajas.com)

## Inspiration

I wanted a simple website that I could make edits to and understand. This is my hand-rolled static website generator.

## Use

If you want to build the website, you can use the included `build` script to generate the site from your clone:

    $ ./build

Note that this relies on some dependencies:
- the macOS `date` binary
- a `mmd` (MultiMarkdown) binary
- `exiftool` (for stripping exif)
- `ffmpeg` (for image recompression)

This will create a new directory called `out`. It's automatically ignored by `git` thanks to a rule in the `.gitignore`.

**Note**: The `build` script will destroy `out` on every run (to make sure everything is fresh). Files left in `out` will be destroyed on runs of `build`.

## Content management

Every `.md` file encountered in the directory (except this readme) will be turned into an `HTML` file. For these files:

- `before.html` will be inserted before their contents
- `after.html` will be inserted after their contents

Every page with a title / date at the beginning of the document matching this format:

    (blank line)
    <!--
    Some title here
    20190106 12:07
    -->

will have the title and date included at the top, and be added to the `index.html` file.
