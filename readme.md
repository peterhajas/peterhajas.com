This repository hosts the content powering [peterhajas.com](http://peterhajas.com)

# Inspiration

I wanted a simple website that I could make edits to and understand. This is my hand-rolled static website generator.

# Use

If you want to build the website, you can use the included `build.py` script to generate the site from your clone:

    $ ./build.py

This will build the contents in `site`.

Note that this relies on `python3` being installed. There are no additional dependencies.

This will create a new directory called `out`. It's automatically ignored by `git` thanks to a rule in the `.gitignore`.

**Note**: The `build.py` script will destroy `out` on every run (to make sure everything is fresh). Files left in `out` will be destroyed on runs of `build.py`.

# Content management

Every `.md` file encountered in the `site` directory  will be turned into an `HTML` file. For these files:

- `before.html` will be inserted before their contents
- `after.html` will be inserted after their contents

Every page with a title / date at the beginning of the document matching this format:

    Title: Some title here
    Date: 20190106 12:07
    Emoji: 👻🦌

will have the title, date, and emoji included at the top, and be added to the `index.html` file.
