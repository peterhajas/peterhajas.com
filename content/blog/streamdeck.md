---
title: "My Custom Stream Deck Toolkit"
date: 2021-08-01T18:05:00-07:00
---

![My Stream Deck and its buttons](/streamdeck/hero.jpeg)

Last September, I bought an [Elgato Stream Deck XL](https://www.elgato.com/en/stream-deck-xl). It's a USB input device with 32 programmable buttons, each with an individual display. I think the target market is video game streamers, who use it to switch cameras, control lighting, play sound effects, and do [star wipe transitions](https://www.youtube.com/watch?v=72bUheqRE5o). I don't stream video games, but I've found myself using the Stream Deck frequently with my computer. This post shows what I'm doing with it and how I built it.

# Hammerspoon and `hs.streamdeck`

I don't use the Elgato Stream Deck software. Instead, I use [Hammerspoon](https://www.hammerspoon.org), the amazing macOS customization tool I've had for years on my systems. You configure it with Lua files, and there is a module for using the Stream Deck called [`hs.streamdeck`](https://www.hammerspoon.org/docs/hs.streamdeck.html). This module lets you:

- run a callback when a Stream Deck is connected or disconnected
- react to button press-down and press-up events
- assign images to buttons
- set brightness

# My Stream Deck Toolkit

{{< video "/streamdeck/nav_stack.mp4" "Navigation Stacks in my toolkit">}}

Using the Hammerspoon support, I built a declarative toolkit for populating the Stream Deck as part of my [dotfiles](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck.lua). I define buttons [as Lua tables with simple properties like `image` and `onClick` callbacks](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/about.md). My toolkit also supports navigation stacks, scrolling, and "panels" - buttons where X and Y on the grid are important (like in the number pad and clone window buttons below). 

This toolkit lets me write buttons very easily, and experiment with new functionality quickly. Making it easy to iterate was essential to my success with this project. For example, the button to lock my computer is a few lines of Lua:

    lockButton = {
        ['name'] = 'Lock',
        ['image'] = streamdeck_imageFromText('🔒'),
        ['onClick'] = function()
            hs.caffeinate.lockScreen()
        end
    }

(lock emoji added for clarity - I use the `lock.fill` symbol from SF Symbols on my system)

# My Buttons

Here are the buttons I use in my personal configuration at home:

- [Weather](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/weather.lua): loads weather from [wttr.in](https://wttr.in) (and shows a few more places when tapped)
- Calendar [Peek](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/peek.lua): shows today's date and acts as a way to "peek" at my calendar. These peek buttons have some *very useful* behavior which I am proud of:
    - when *pressed*, they will show Calendar if it is not frontmost, or hide it if it is frontmost
    - when *held*, they will show Calendar _only while held_, hiding it when released

    These make it really easy to check my Calendar during a meeting, or quickly see what my next day looks like.

- Reeder Peek: peeks at Reeder, my feed reader
- [Lock](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/lock.lua): locks my Mac when pressed
- [Audio](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/audio_devices.lua): shows my connected output and input devices. This helps when switching between audio devices during meetings. These buttons also show a little bar indicating the selected device's current volume (dimmed if it does not support volume)

    ![My audio output and audio input buttons](/streamdeck/audio_switcher.jpeg)

- [Media Controls](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/itunes.lua): Skips tracks. I don't use these very much
- [App Switcher](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/app_switcher.lua): Pushes a grid of open apps onto the navigation stack. Each of these buttons act as peek buttons for that app
- [Window switcher](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/window_switcher.lua): Pushes a grid of open windows, with snapshots and app icons, onto the navigation stack. Pushing one of these makes that window frontmost
- [Home Assistant](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/home_assistant.lua): Pushes a grid of all my Home Assistant entities onto the navigation stack. This lets me control lights, switches, scenes, run scripts, etc.
- [Numpad](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/numpad.lua): Pushes a panel which is a software number pad / calculator for the currently foreground app

    ![The numberpad button panel](/streamdeck/number_pad.jpeg)

- [Window Clone](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/window_clone.lua): Pushes a grid of open windows onto the navigation stack. Selecting one pushes a panel-based live-updating version of it on the Stream Deck. This can be handy for keeping an eye on something, and lets the Stream Deck act as a slow-updating external display for a window

    ![A Window Zoom panel showing peterhajas.com](/streamdeck/window_zoom.jpeg)

- [Function Keys](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/function_keys.lua): Pushes a grid of software F-keys, going from F1 to F20

    ![The software function keys grid](/streamdeck/function_keys.jpeg)

- Office Regular, Office Mood, Office Off: Each of these act as shortcuts to activate a specific Home Assistant scene in my office
- [Shortcuts](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/shortcuts.lua): Pushes a grid of my Shortcut folders onto the navigation stack. From these, I can pick a Shortcut and run it from the Stream Deck
- [Camera 1, Camera 2, Dash Close](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/camera.lua): Shows a camera feed from an external camera on my "dash" display in my office (a subject of a future post). The "dash close" button lets me close any open windows on my dash display
- [Shelf A, B, and C](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/shelf.lua): lets me store anything on the clipboard into a scratch buffer and later recall it by pressing the button. Holding the button clears that buffer

The colored buttons at the bottom are [nonce buttons](https://github.com/peterhajas/dotfiles/blob/master/hammerspoon/.hammerspoon/streamdeck/nonce.lua). They show a random color and cycle between it at an interval, because it looks cool.

If you like what you see, or if you end up using my toolkit, please [write me an email](/about)!

