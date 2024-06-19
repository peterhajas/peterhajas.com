---
title: "Per-Tiddler Custom CSS Styling"
date: 2024-06-19T10:55:09-06:00
---

I really enjoy how extensible TiddlyWiki is. You can easily modify the tool to suit your need.

One thing I found myself doing with my notes is wanting to style tags or tiddlers individually. For example, all tiddlers tagged "Public" show up with a faint green hue to remind myself that they're public and readable by anyone. Tiddlers tagged "phajas" (generally all my "personal" or meta tiddlers) get an orange top line.

Rather than do this manually with stylesheet tiddlers, I wrote a utility tiddler that handles this **automatically**. Here it is:

```
\whitespace trim
<$list filter="[is[tiddler]]">

<$list filter="[<currentTiddler>fields[]prefix[css]!suffix[css]]" variable="field">
<$let
CSSPROP={{{ [<field>search-replace[css-],[]] }}}
VALUE={{{ [<currentTiddler>get<field>] }}}
>

[data-tiddler-title="<<currentTiddler>>"] {
  <<CSSPROP>> : <<VALUE>>;
}

.tc-tagged-<<currentTiddler>> {
  <<CSSPROP>> : <<VALUE>>;
}

</$let>
</$list>

</$list>
```

(put this in a Tiddler tagged `$:/tags/Stylesheet`).

In any tiddler or tag where you want custom styling, add a `css-` prefixed field with the value. For example, adding this to a Tag tiddler:

```
css-background-color: {{!!color}}33
```

will add a partially translucent background matching that tag's color. Notice how we can transclude the color field. You can also impress your friends by adding:

```
css-font-family: Papyrus
```

to a tiddler to give it some swanky styling.
