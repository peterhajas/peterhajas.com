Title: Visualizing Pokémon Red and Blue Connections
Date: 20200414 20:45
Emoji: 😺🗺

I love Pokémon. My fascination with the series began with the original games released in the US, Pokémon Red and Blue (I had the Blue version).

In the past few years, people have been disassembling Pokémon games. You can check these out for Pokémon [Red and Blue](https://github.com/pret/pokered), [Crystal](https://github.com/pret/pokecrystal), [Emerald](https://github.com/pret/pokeemerald), and others. It's really cool to be able to compile and build a game that was such a huge part of my youth.

I thought it would be fun to play with this source code, viewing these games through a new lens. A few months ago, I discovered [Graphviz](https://www.graphviz.org), a software package for rendering graphs written in the [Dot language](https://en.wikipedia.org/wiki/DOT_(graph_description_language)). Dot is a very simple language, and it's easy to filter data into its format. Graphviz includes some command line tools that can render dot files to nice human-readable output. Let's see how we can use Graphviz to visualize Pokémon Red and Blue.

Inside of `pokered`, there's a `data` directory with a `mapHeaders` subdirectory inside. `mapHeaders` includes metadata about every overworld map in the game. This includes the connections between maps. For example, here is the metadata for Route 10:

    $ cat Route10.asm 
    Route10_h:
        db OVERWORLD ; tileset
        db ROUTE_10_HEIGHT, ROUTE_10_WIDTH ; dimensions (y, x)
        dw Route10_Blocks ; blocks
        dw Route10_TextPointers ; texts
        dw Route10_Script ; scripts
        db SOUTH | WEST ; connections
        SOUTH_MAP_CONNECTION ROUTE_10, LAVENDER_TOWN, 0, 0, LavenderTown_Blocks
        WEST_MAP_CONNECTION ROUTE_10, ROUTE_9, 0, 0, Route9_Blocks
        dw Route10_Object ; objects

So south of Route 10 is Lavender Town, and west is Route 9. We can use this connection data and some simple uses of `grep` and `awk` to generate Dot code representing these connections. The following commands are all run from `/data/mapHeaders` in the `pokered` repository. First, we use `grep` to see the connections:

    $ grep -R "MAP_CONNECTION" ./
    .//PewterCity.asm:	SOUTH_MAP_CONNECTION PEWTER_CITY, ROUTE_2, 5, 0, Route2_Blocks
    .//PewterCity.asm:	EAST_MAP_CONNECTION PEWTER_CITY, ROUTE_3, 4, 0, Route3_Blocks
    ...
Next, let's pipe that to `awk` to print the endpoints of that connection:

    $ grep -R "MAP_CONNECTION" ./ | awk -F" " '{ print $3 $4; }'
    PEWTER_CITY,ROUTE_2,
    PEWTER_CITY,ROUTE_3,
    ...

We can use a second `awk` invocation to print these as Dot edges:

    $ grep -R "MAP_CONNECTION" ./ | awk -F" " '{ print $3 $4; }' | awk -F"," '{ print $1" -- "$2 }'
    PEWTER_CITY -- ROUTE_2
    PEWTER_CITY -- ROUTE_3
    ...

Undirected Dot edges are represented with the two nodes and a `--` between them.

We can represent a strict (one connection between nodes) graph (non-directed, as these are bidirectional connections) by wrapping all these connections in a `strict graph {}`:

    strict graph {
        PEWTER_CITY -- ROUTE_2
        PEWTER_CITY -- ROUTE_3
        ...

We can add two other options (`overlap=false` to avoid edge overlap and `splines=true` to use splines for edges) to get a better looking graph. Here's my `pokemon_rb_towns_and_routes.dot` generated from the above steps:

    strict graph {
        overlap=false;
        splines=true;
        PEWTER_CITY -- ROUTE_2
        PEWTER_CITY -- ROUTE_3
        CELADON_CITY -- ROUTE_16
        CELADON_CITY -- ROUTE_7
        ROUTE_9 -- CERULEAN_CITY
        ROUTE_9 -- ROUTE_10
        ROUTE_8 -- SAFFRON_CITY
        ROUTE_8 -- LAVENDER_TOWN
        ROUTE_21 -- PALLET_TOWN
        ROUTE_21 -- CINNABAR_ISLAND
        ROUTE_20 -- CINNABAR_ISLAND
        ROUTE_20 -- ROUTE_19
        ROUTE_22 -- ROUTE_23
        ROUTE_22 -- VIRIDIAN_CITY
        PALLET_TOWN -- ROUTE_1
        PALLET_TOWN -- ROUTE_21
        ROUTE_23 -- INDIGO_PLATEAU
        ROUTE_23 -- ROUTE_22
        VERMILION_CITY -- ROUTE_6
        VERMILION_CITY -- ROUTE_11
        ROUTE_24 -- CERULEAN_CITY
        ROUTE_24 -- ROUTE_25
        ROUTE_18 -- ROUTE_17
        ROUTE_18 -- FUCHSIA_CITY
        ROUTE_19 -- FUCHSIA_CITY
        ROUTE_19 -- ROUTE_20
        ROUTE_25 -- ROUTE_24
        LAVENDER_TOWN -- ROUTE_10
        LAVENDER_TOWN -- ROUTE_12
        LAVENDER_TOWN -- ROUTE_8
        ROUTE_14 -- ROUTE_15
        ROUTE_14 -- ROUTE_13
        ROUTE_15 -- FUCHSIA_CITY
        ROUTE_15 -- ROUTE_14
        ROUTE_17 -- ROUTE_16
        ROUTE_17 -- ROUTE_18
        ROUTE_16 -- ROUTE_17
        ROUTE_16 -- CELADON_CITY
        ROUTE_12 -- LAVENDER_TOWN
        ROUTE_12 -- ROUTE_13
        ROUTE_12 -- ROUTE_11
        ROUTE_13 -- ROUTE_12
        ROUTE_13 -- ROUTE_14
        ROUTE_11 -- VERMILION_CITY
        ROUTE_11 -- ROUTE_12
        CERULEAN_CITY -- ROUTE_24
        CERULEAN_CITY -- ROUTE_5
        CERULEAN_CITY -- ROUTE_4
        CERULEAN_CITY -- ROUTE_9
        ROUTE_10 -- LAVENDER_TOWN
        ROUTE_10 -- ROUTE_9
        ROUTE_5 -- CERULEAN_CITY
        ROUTE_5 -- SAFFRON_CITY
        FUCHSIA_CITY -- ROUTE_19
        FUCHSIA_CITY -- ROUTE_18
        FUCHSIA_CITY -- ROUTE_15
        SAFFRON_CITY -- ROUTE_5
        SAFFRON_CITY -- ROUTE_6
        SAFFRON_CITY -- ROUTE_7
        SAFFRON_CITY -- ROUTE_8
        ROUTE_4 -- ROUTE_3
        ROUTE_4 -- CERULEAN_CITY
        ROUTE_6 -- SAFFRON_CITY
        ROUTE_6 -- VERMILION_CITY
        VIRIDIAN_CITY -- ROUTE_2
        VIRIDIAN_CITY -- ROUTE_1
        VIRIDIAN_CITY -- ROUTE_22
        INDIGO_PLATEAU -- ROUTE_23
        ROUTE_7 -- CELADON_CITY
        ROUTE_7 -- SAFFRON_CITY
        ROUTE_3 -- ROUTE_4
        ROUTE_3 -- PEWTER_CITY
        ROUTE_2 -- PEWTER_CITY
        ROUTE_2 -- VIRIDIAN_CITY
        CINNABAR_ISLAND -- ROUTE_21
        CINNABAR_ISLAND -- ROUTE_20
        ROUTE_1 -- VIRIDIAN_CITY
        ROUTE_1 -- PALLET_TOWN
    }

We can use a simple invocation of `neato` to produce a PDF file with:

    neato -Tpdf pokemon_rb_towns_and_routes.dot > pokemon_rb_towns_and_routes.pdf

Check it out:

![A graph visualizing all towns and routes in Pokémon Red and Blue](/media/pokemon_rb_towns_and_routes_preview.png)
([PDF file here](/media/pokemon_rb_towns_and_routes.pdf))

OK, so towns and routes are cool. Can we augment this file to include buildings, tunnels, and rooms? There are `warp` and `warp_to` markers in the files in `/data/mapObjects`. For example, let's look at `SaffronCity.asm`:

    $ cat data/mapObjects/SaffronCity.asm
    SaffronCity_Object:
        db $f ; border block

        db 8 ; warps
        warp 7, 5, 0, COPYCATS_HOUSE_1F
        warp 26, 3, 0, FIGHTING_DOJO
        warp 34, 3, 0, SAFFRON_GYM
        warp 13, 11, 0, SAFFRON_PIDGEY_HOUSE
        warp 25, 11, 0, SAFFRON_MART
        warp 18, 21, 0, SILPH_CO_1F
        warp 9, 29, 0, SAFFRON_POKECENTER
        warp 29, 29, 0, MR_PSYCHICS_HOUSE

        ...

        ; warp-to
        warp_to 7, 5, SAFFRON_CITY_WIDTH ; COPYCATS_HOUSE_1F
        warp_to 26, 3, SAFFRON_CITY_WIDTH ; FIGHTING_DOJO
        warp_to 34, 3, SAFFRON_CITY_WIDTH ; SAFFRON_GYM
        warp_to 13, 11, SAFFRON_CITY_WIDTH ; SAFFRON_PIDGEY_HOUSE
        warp_to 25, 11, SAFFRON_CITY_WIDTH ; SAFFRON_MART
        warp_to 18, 21, SAFFRON_CITY_WIDTH ; SILPH_CO_1F
        warp_to 9, 29, SAFFRON_CITY_WIDTH ; SAFFRON_POKECENTER
        warp_to 29, 29, SAFFRON_CITY_WIDTH ; MR_PSYCHICS_HOUSE

        ...

(These `_WIDTH` suffixes seem to indicate the coordinates are inside of the width of the map. We'll clean them up later.)

So, if we parse out the `warp_to` statements, we should be able to get a more complete view of the game's locations and how they connect. Let's start with a simple `grep` to find all the `warp_to` statements (run from `/data/mapObjects`):

    grep -R "warp_to " ./
    .//RocketHideoutB4F.asm:	warp_to 19, 10, ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_B3F
    .//RocketHideoutB4F.asm:	warp_to 24, 15, ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    .//RocketHideoutB4F.asm:	warp_to 25, 15, ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    ...

Next, pipe to `awk` to find the endpoints of the warp:

    $ grep -R "warp_to " ./ | awk -F"," '{ print $3; }'
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_B3F
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    CELADON_MART_3F_WIDTH ; CELADON_MART_4F
    CELADON_MART_3F_WIDTH ; CELADON_MART_2F
    CELADON_MART_3F_WIDTH ; CELADON_MART_ELEVATOR
    BRUNOS_ROOM_WIDTH ; LORELEIS_ROOM
    BRUNOS_ROOM_WIDTH ; LORELEIS_ROOM
    BRUNOS_ROOM_WIDTH ; AGATHAS_ROOM
    BRUNOS_ROOM_WIDTH ; AGATHAS_ROOM
    BIKE_SHOP_WIDTH
    ...

This is close, but includes some warps that appear to point to themselves (like `BIKE_SHOP_WIDTH` above). No problem - we can only print lines with `;` in them using `grep`:

    $ grep -R "warp_to " ./ | awk -F"," '{ print $3; }' | grep ";"
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_B3F
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    ROCKET_HIDEOUT_B4F_WIDTH ; ROCKET_HIDEOUT_ELEVATOR
    CELADON_MART_3F_WIDTH ; CELADON_MART_4F
    CELADON_MART_3F_WIDTH ; CELADON_MART_2F
    CELADON_MART_3F_WIDTH ; CELADON_MART_ELEVATOR
    ...

OK, almost done. Next, let's strip out the `_WIDTH` text and put in edge connections:

    $ grep -R "warp_to " ./ | awk -F"," '{ print $3; }' | grep ";" | sed -e "s/_WIDTH//" | sed -e "s/;/--/"
     ROCKET_HIDEOUT_B4F -- ROCKET_HIDEOUT_B3F
     ROCKET_HIDEOUT_B4F -- ROCKET_HIDEOUT_ELEVATOR
     ROCKET_HIDEOUT_B4F -- ROCKET_HIDEOUT_ELEVATOR
     CELADON_MART_3F -- CELADON_MART_4F
     CELADON_MART_3F -- CELADON_MART_2F
     CELADON_MART_3F -- CELADON_MART_ELEVATOR
    ...

(note the leading space here - not a big deal for the Graphviz tools)

Now, we'll put this all into a `pokemon_rb_all.dot` file (along with the connections from `pokemon_rb_towns_and_routes.dot`) to make a graph of all of the locations in Pokémon Red and Blue. For this invocation, I also used `neato`:

    neato -Tpdf pokemon_rb_all.dot > pokemon_rb_all.pdf

This graph is so cool! Check it out:

![A graph visualizing all locations in Pokémon Red and Blue](/media/pokemon_rb_all_preview.png)
([PDF file here](/media/pokemon_rb_all.pdf), [dot file here](/media/pokemon_rb_all.dot))

There are so many sections of this graph with interesting details, like Victory Road leading into the Indigo Plateau and Elite Four:

![A cropped version of the "all locations" graph showing just Victory Road, the Indigo Plateau, and the Elite Four sections of the graph](/media/pokemon_rb_all_e4.png)

Or the maze-like Silph Company building:

![A cropped version of the "all locations" graph showing just the Silph Company building floors](/media/pokemon_rb_all_silph.png)

I think it's really cool how easy it is to use simple tools to see these games from a new angle. I hope to look at other aspects of these games sometime in the future.
