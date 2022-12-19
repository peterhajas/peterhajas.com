Title: Peterometer
Date: 20221218 06:10

i've written a few times on this site about the Peterometer, my name for a quantified-self dashboard.

Over the recent Thanksgiving holiday, I worked on [a new version of the Peterometer](/peterometer/) that I'm ready to share.

[![An image of the peterometer](/media/peterometer.jpeg)](/peterometer/)

# Inspiration

The site is themed after the visuals in the 2013 film [Oblivion](https://en.wikipedia.org/wiki/Oblivion_(2013_film)), which is a great movie with excellent futuristic UI (and music). I found [a page](https://gmunk.com/OBLIVION-GFX) by one of the visual artists explaining how they built the UI for the movie. I like the clean lines, simple colors, and graphs. I used this as inspiration for building the website itself - a cool futuristic font, a neat color palette, and 3D graphics animating in a subtle way.

I got feedback from friends and family - thanks to [James](https://buzzert.net) and [Charles](http://zanneth.com) for pushing me to use a consistent palette, and thanks to my sister for pointing out that my previously chosen palette was ugly.

I listened to the [TRON: Legacy soundtrack](https://en.wikipedia.org/wiki/Tron:_Legacy_(soundtrack)) while working on this site.

# The Data

I log a lot of data about myself:

* Health data automatically through my watch, which I've worn since April 2015
* Food, which I have logged since March 2019
* Hydration, which I have logged since December 2018

It's not hard or irritating for me to log when I eat or drink, and it makes me more mindful of what I *do* end up ingesting.

The site is populated by the [Health Auto Export](https://www.healthexportapp.com) app, which runs in the background on my phone. It takes my HealthKit database and periodically slurps up the last 7 days of data and sends it to the website. I like this because I don't have to think about the site at all - I just log data like I normally do, and it shows up on the Peterometer after a few days. I like that the Peterometer fits seamlessly into habits I've already built.

# The Site

I use the [Three.js](https://threejs.org) library for rendering the 3D data. I wrote some code to line up Three.js objects with DOM elements, which made it easy to use flexbox to position the elements of the site. The site is responsive to window size changes.

# Next Steps

I have a 3D scan of my body that I'd like to add to the page. I wish I could use a tool like `ffmpeg` to downsize the model, make it low-poly, and put it on the site. If you know how to do this, email me!

I would also like to have a display in my home dedicated to showing this information. It would be nice to see this as a kind of "Peter Health Dashboard" throughout the day, and it may end up influencing my behavior.
