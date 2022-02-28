Title: Pokémon Map Generator
Date: 20220227 20:00
Emoji: 🤖🗺

<center class="pokemon_map_generator_shots">
![A map with caves in a city](/media/pokemon_map_generator/cave_city.png)
</center>

[The generator is available on my website here](/pokemon_mapgen).

I recently took a week long vacation. I love working on recreational programming projects during a vacation. It's a great chance to try programming in a space I am less familiar with.

This vacation, I worked on something I've wanted for a long time: a Pokémon map generator! I've always been interested in the maps in the Game Boy Pokémon games (read more about [parsing the data format](/blog/pokemon_rb_map_parsing.html) and [visualizing the map connections](/blog/pokemon_rb_connections.html)). There was something magical about exploring these areas, pouring over towns in strategy guides, and designing my own maps on paper.

# Generated Maps

I love looking at the maps you can generate with this. Here are a few of them that stood out to me:

<center class="pokemon_map_generator_shots">
A Town with a Cave
![A map with a cave next to a town with large buildings](/media/pokemon_map_generator/cave_town.png)
Shop by the Sea
![A map with a shop near the water](/media/pokemon_map_generator/shop_by_the_sea.png)
Skyscraper By a Lab
![A map with a lab next to a skyscraper](/media/pokemon_map_generator/skyscraper_by_lab.png)
Mountain Route
![A route map with mountains next to it](/media/pokemon_map_generator/mountain_route.png)
The Super Nintendo Room
![A map with a bunch of Super Nintendo consoles on tables](/media/pokemon_map_generator/snes_room.png)
</center>

# The Algorithm

In addition to letting you visualize maps from Pokémon Red and Blue, this site also lets you generate your own maps using a (naive) [Markov](https://en.wikipedia.org/wiki/Markov_chain)-style approach.

Here's how it works:

- I wrote a small python program to gather data from the [pokered repository](plh-evil) in JSON format. It scrapes out the built-in maps and their metadata, the blocksets, and the tilesets.
- When you click "Generate", we find all the maps in Pokémon that have the tileset you chose.
- For each of these maps, we record their blocks and what blocks neighbor them. For example, if block `77` in `OVERWORLD` has block `12` north of it in a map, we record this. I also record the frequency that these blocks occur, but this is not currently used in map generation. These neighbors are stored in a dictionary.
- Starting from the top-left, we choose a random block that is known to be used by maps with this tileset. These are just the keys for the above neighbors dictionary.
- We then fill the map from left to right, top to bottom, trying to find blocks that can fit in with the constraints of the already built map. If the map is unsatisfiable, it's thrown out and we attempt again (up to 2000 iterations - and we may sometimes never find a solution). This is part of the generation algorithm that I'd like to improve and get feedback on.
- Once the map is complete, we render it using the techniques described below.

Note that it has bugs! I'd recommend not getting larger than 8x8 for most tilesets. Some tilesets are missing, like "DOJO" and "REDS_HOUSE".

# Rendering Maps

To render both built-in and generated maps, the site uses a similar mechanism to my Emoji-based approach (although much faster than rendering all that unicode!). It parses the tileset and blocksets, and renders them using [`<canvas>`](http://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas) into an image element. This is great for saving the map for use offline.

Because of my very fond nostalgia for the [Game Boy Color](https://en.wikipedia.org/wiki/Game_Boy_Color), I also added support for rendering using multiple palettes. The Game Boy Color could [switch palettes](https://en.wikipedia.org/wiki/Game_Boy_Color#Color_palettes) based off of the button combination you held down when it booted. As a kid, I found it fun to hold down the buttons and see what cool palettes I could see Pokémon in. I also added a "grayscale" and "gameboy" palette for completeness - you can see maps rendered in their green original Game Boy glory!

---

I had fun building this generator, and I hope you have fun playing with it! [Get in touch](/about.html) if you have questions, feedback, or if you generate any really cool maps!

