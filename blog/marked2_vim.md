
<!--
Live Markdown previews from vim
20190106 12:07
-->

*This is more of a technical post*

This site is written using [Markdown](https://daringfireball.net/projects/markdown/), which:

> allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML)

It's a common technique for writing blogs, as it lets the author write text in the text editor of their choice.

I write this page in `vim`, which is a command line text editor. I love `vim` for many reasons that are outside the scope of this post. I've been using it as my primary editor for almost 5 years. I wanted a good solution for writing Markdown in `vim`.

Because `vim` is a command line editor, it makes it tougher to use it to write rich text. In a GUI program, rich text can be rendered inline and as-you-edit. A command line tool can show you the formatting you have applied to text, but it does not give you an accurate rendering of how your content will look as you edit it.

I wanted to continue to use `vim` to edit my blog posts (I find `vim` plugins for other editors to be a worse approximation than "I can't believe it's not butter"). This post is about how I solved this problem.

#### A Markdown preview app

On macOS, you can get apps to render Markdown in a window. One that I like a lot is [Marked](http://marked2app.com), which automatically refreshes its preview when the Markdown file changes. This means you can open a `.md` file in Marked and get live updates *as you change it*. This can be used with any editor, including `vim`. The flow is something like:

- `touch` or `:e` the file you want to write
- Open Marked
- Open the file in Marked

As you save to it with `:w`, the preview will be auto-refreshed. I like this, but wanted to open it with a single key combination.

#### Adding Marked to `vim`

We can write a `vim` function to help us with this. Something like this:

    function OpenInMarked2()
        " Open the file in Marked here
    endfunction

##### Running a shell command from `vim`

We can use `!` to run a command from our function. Technically, this is the `filter` command. From `:help !`:

> `!{motion}{filter}` Filter `{motion}` text lines through the external program `{filter}`.

You can try this in your `vim`. Just run `:!pwd,` and you should be presented with your shell and your current working directory. Below it, `vim` helpfully tells us "Press ENTER or type command to continue".

This is great! Using this and the macOS `open` command, we can at least *launch* Marked 2 with something like this:

    !open -a Marked\ 2.app

But what about opening the current file? `vim` lets us use `%` from Ex commands as a stand-in for the path to the current file. So we can do something like:

    !echo %

to see the current file. We can use this with `open` to open the current file in `vim`:

    !open -a Marked\ 2.app %

This is the body of our `OpenInMarked2` function:

    function OpenInMarked2()
        !open -a Marked\ 2.app %
    endfunction

Once we have this function, we can call it with the Ex `call` command, like this:

    :call OpenInMarked2()

This will open the current file in Marked, but will leave us at the shell with "Press ENTER or type command to continue" there. We still have to press enter before we can edit the file live.

##### Defining a mapping

We can use a `vim` mapping to call the function for us. A mapping lets us take a key combination and map it to a command. For the key combination, I like to use `<leader>`, which is a user-controlled modifier in `vim`. This means that `<leader> _` is wide open for use in your `.vimrc`. For my `leader` key, I use `,` (comma), as it's near the other modifiers on a US keyboard. For `leader` mappings, I like a mnemonic key combination, as it makes it easier to remember.

A good choice for this mapping, which is applicable for **M**arkdown and for opening **M**arked, is `<leader>m`. Our mapping to call the function might look like this:

    nmap <silent> <leader>m :call OpenInMarked2()

Here's a decoder ring for what these commands mean:

    - `nmap` means a mapping that exists in `vim`'s normal mode
    - `<silent>` means the mapping will not be echoed on the command line
    - `<leader>m` is the mapping we've picked for this particular command
    - `:call` will call a particular function
    - `OpenInMarked2()` is the name of the function we'd like to call

If you add this mapping and function to your `.vimrc`, you'll see that it works *kind of*. You have to hit enter to get the command to actually run, and then after doing so you're left at the shell, so you need to hit enter **again** before returning to the editor.

##### Hitting enter twice

We can add a press of the enter key to our mapping using `<CR>`. This acts as though the user has pressed the carriage return. We'll add two of them, as we need one to run the function and another to return to the editor. Our mapping now looks like this:

    nmap <silent> <leader>m :call OpenInMarked2() <CR> <CR>

which is the mapping you'll find in my [`.vimrc`](https://github.com/peterhajas/dotfiles/blob/master/vim/.vimrc).

---

I hope you found this post helpful. I have been using `OpenInMarked2` to help me write Markdown for 2 years now, and I think it's a cool example of how to extend `vim` to fit your needs.
