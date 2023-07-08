---
title: Internet Independence
---

This is a page with some tips and tricks for being more independent on the internet.

# Independence for stuff you consume

The internet has all sorts of stuff to consume. For example:

- news sites
- aggregator sites (Reddit, Hacker News)
- social media sites
- video sites

Thankfully, you can subscribe to all of these with feeds!

## The Power of Feeds

Feeds are a neat way to subscribe to content on the web. You can subscribe to a site in your [feed reader](https://www.youneedfeeds.com/web-based) and get updates from it. This way, when you want to check on things, you only need to open your feed reader. This also lets you avoid many forms of tracking.

Under the hood, "Atom" and "RSS" are the dominant feed standards on the web. [You can read more about feeds on this page](https://aboutfeeds.com).

### Sites that Support Feeds

Most sites support feeds out of the box. For example, if you want to read posts from [Slashdot](https://slashdot.org), you can subscribe to their [RSS feed](http://rss.slashdot.org/Slashdot/slashdotMain) and read posts in your feed reader.

Here are some tips for using RSS on some sites you may already use:

#### Hacker News

[Hacker News RSS Feed](https://news.ycombinator.com/rss)

[n-gate](http://n-gate.com) also has an [RSS Feed](http://n-gate.com/index.rss)

#### Reddit

Subreddits can be subscribed to with RSS using `https://old.reddit.com/r/the_subreddit_here/.rss`.

#### YouTube

To get any YouTube channel's RSS feed:

1. Go to the channel
2. View the page source 
3. Look for the `application/rss+xml` link in the source. The feed link should look like `https://www.youtube.com/feeds/videos.xml?channel_id=THE_CHANNEL_ID_IS_HERE` 

You can also export your YouTube subscriptions as an OPML file that you can import into your feed reader by going to the [Subscription Manager](https://www.youtube.com/subscription_manager) and clicking "Export subscriptions" at the bottom of the page. See [this Google Support](https://support.google.com/youtube/answer/6224202?hl=en) article for more.

### Other Sites

Not all sites support feeds out of the box, but there is usually a way to subscribe. For example, you can use [RSSHub](https://github.com/DIYgod/RSSHub) or [rss-bridge](https://github.com/RSS-Bridge/rss-bridge) to get feeds for other sites.

#### Twitter

While Twitter doesn't support RSS, there's a great way to subscribe to Twitter pages via [nitter](https://nitter.net). You can replace any `twitter.com` URL with `nitter.net`. Nitter exposes RSS feeds for individual users. For example, my Twitter profile's RSS feed is at [https://nitter.net/peterhajas/rss](https://nitter.net/peterhajas/rss).

# Independence for stuff you produce

It's also fun to share stuff with your friends, family, and the world.

## Get a Website

You should [get a website](/blog/get_a_website)! It's nice to put your stuff on a platform you control. You can put your writing, your photos, and other stuff you want to share on your own website.

Once you've gotten a website, it's a good idea to publish your content with feeds. This lets people subscribe using their feed reader. Your website might already support feeds depending on how it is configured (like if you're using Wordpress, Jekyll, or Hyde). If not, you can check out the [Atom](https://en.wikipedia.org/wiki/Atom_(Web_standard)) and [RSS](https://en.wikipedia.org/wiki/RSS) standards on Wikipedia and try your hand at generating your own. This site generates its own RSS feed.

