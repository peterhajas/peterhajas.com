Title: Avoiding Ads
Date: 20220715 20:45

I hate ads. I don't like watching them, I don't like seeing them, and I don't like hearing them. The attention economy is very sad and I want no part of it. "Ethical ads" are about as oxymoronic as "healthy cigarettes". A [friend](https://buzzert.net) recently told me that advertising [reduces activity in the decision-making parts of your brain](https://www.sciencedaily.com/releases/2011/09/110920163318.htm).

Funnily enough, the more visual ads are, the easier they are to avoid. Here is how I avoid most advertisements.

# Avoiding Audio Ads

This one is easiest to set up. Most podcatchers support a different "Skip Forward" and "Skip Backward" duration. Everyone I know who listens to podcasts has these set to "Skip forward 30 seconds" and "Skip backward 15 seconds". Each time you hear the start of an ad about a great new mattress (that the hosts only ever have in their guest room), or a non-FDA approved CBD vendor, you skip forward 30 seconds. You keep pressing this until the show - the thing you're there to listen to - comes back on, and then you back up by 15 seconds until you're between the ad and the show.

Usually this means you're still subject to "thanks to our friends at ___" narration, perhaps with a coupon code, but it's better than listening to the whole ad.

# Avoiding Web Ads

This one takes a bit more effort, depending on how far you want to go. I use ad blockers (extensions that run on your device) to block web ads. These involve filters or rules to omit content from webpages before it is rendered (or in some cases fetched). I use 12+ of these on my devices.

I also run [pihole](https://pi-hole.net) on a computer in my house, and route all my internet traffic through it. This filters out content before devices fetch it by blocking the domain name resolution of advertising and analytics. This accounts for a shockingly high 8% of all domain queries on my network.

# Avoiding Video Ads

This one takes the most effort to configure, but it's well worth the setup time. I love web video, but hate the ads that hosting providers and content creators sprinkle in their videos. For avoiding ads that the site inserts (usually for vacation rentals and car insurance), I use `yt-dlp`. This program downloads a video to your local computer, and you never need to see the pre-roll / mid-roll ads the hosting provider inserts.

To avoid ads that content creators place in the middle of their videos (for VPN services and wallets, usually), I use the `--sponsorblock-remove` flag of `yt-dlp`. There's a community-maintained database of ad segments of videos called [SponsorBlock](https://sponsor.ajay.app). The `--sponsorblock-remove` flag hits this database, finds the time codes for the ad segments, and then *stitches them out of the video file*. This feature is awesome, and there's a [list of the different types](https://wiki.sponsor.ajay.app/w/Guidelines) of video segments that SponsorBlock can stitch out.

I've mapped my invocation of `yt-dlp` to a simple hotkey, so with one keypress I can download and watch (ad free!) any video link in my clipboard.

<hr>

I hope this article was helpful for avoiding ads in your day-to-day life. These techniques help me move through the cloud of engagement metrics and sketchy tracking, and towards a place where I own my time and attention.
