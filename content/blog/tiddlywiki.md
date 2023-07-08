---
title: "The Recursive Power of TiddlyWiki"
date: 2022-06-02T22:22:00-07:00
---

I recently learned about [TiddlyWiki](https://tiddlywiki.com). It's wiki software that you run on your computer.

There are lots of these "second brain" pieces of software - Notion, Obsidian, vimwiki. But TiddlyWiki has some special tricks up its sleeve that I think put it into a league of its own. There are two components of it that I find so intriguing.

# It includes its own viewer and editor

If I were using vimwiki (which I used to, heavily!), I'd store all my files on my computer (like in `~/.vimwiki`, which I had symlinked to my NextCloud instance). But I'd need a way to view and edit those files. I used `vim` and Marked 2. TiddlyWiki is a self-contained HTML file. It has everything in it - the editor, the viewer, a filesystem implementation, but it's all saved to one HTML file. This is very novel - it's the ultimate portability. I can sync one file to copy my entire database, viewing experience and all. I can make copies of to back it up or try new things.

# It is built in itself

This TiddlyWiki's superpower. It is a tool that is built inside of itself. Besides a small kernel of core functionality, the rest of the system is represented as "tiddlers" - individual notes / files. The sidebar menu, the story list of tiddlers, the editor toolbar, *all of this* is represented as Tiddlers. This makes it very easy to add new functionality to these views. For example, I added an Emoji picker and indicator to all my Tiddlers in a few minutes. This can be done with the embedded powerful template language. TiddlyWiki supports key-value storage (called "fields") on tiddlers, enabling you to make your own taxonomy and relationships.

To help you wrap your mind around this concept, here are things that are _just tiddlers_ in TiddlyWiki:

- the menus and user interface
- the stylesheets that customize the UI
- the user settings (metrics, themes, behaviors)
- the state of the wiki, like open tiddlers
- plugins, which can contain JavaScript, CSS, and tiddlers
- keyboard shortcuts, including the ability to make your own

Much of this UI comes from use of tags, which is just another field on a tiddler. This lets you put things into the system easily. If you want a new item in the sidebar, just tag it with `$:/tags/SideBarSegment`. If you want something new in the view for each tiddler, tag it with `$:/tags/ViewTemplate`.

<hr>

I found this software a few days ago, and I've already become enamored with it. I think this site might eventually become a TiddlyWiki.

As they say in their [Discover](https://tiddlywiki.com/static/Discover%2520TiddlyWiki.html) page:

> You've never seen anything like TiddlyWiki

I agree - I recommend you [go play with it](https://tiddlywiki.com)!
