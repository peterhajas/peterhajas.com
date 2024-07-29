#!/bin/bash

echo "PREPARING"
TIDDLYWIKI="tiddlywiki +plugins/tiddlywiki/markdown --verbose"

echo "CLEANING UP"
rm /out/*
rm -r /out/*

echo "EXPORTING"
$TIDDLYWIKI --load /wiki/wiki.html --output /tmp/ --render '.' public.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]]:or[tag[phajas]]:or[prefix[$:/phajas]]:except[tag[Private]]'

echo "STRIPPING PUBLIC TAGS"
/tiddlywiki_strip_public_tag /tmp/public.json

echo "IMPORTING INTO BASE WIKI"
$TIDDLYWIKI --load /base.html --import /tmp/public.json application/json --output /tmp/ --render "\$:/core/save/all" "/out/out.html" "text/plain"

echo "GENERATING STATIC VARIANT"
mkdir -p /out/static

# HTML representations of individual tiddlers
$TIDDLYWIKI --load /out/out.html --rendertiddlers '[!is[system]]' $:/core/templates/static.tiddler.html /out/static text/plain

# CSS
$TIDDLYWIKI --load /out/out.html --rendertiddler $:/core/templates/static.template.css /out/static/static.css text/plain

# TiddlyWiki likes to take ownership over the directory it operates in, which
# is fine. To help us get the behavior we want with images, move things up a
# level so they're all in `/out/` (and nix `/out/static`).
mv /out/static/* /out/
rm -r /out/static

echo "GRABBING PUBLIC EXTERNAL ASSETS"
$TIDDLYWIKI --load /wiki/wiki.html --output /tmp/ --render '.' external_assets.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]has[_canonical_uri]]'

cat /tmp/external_assets.json | jq -r '.[] | ._canonical_uri' | sed 's/%20/ /g' | while read -r uri; do
  dir_path="/out/$(dirname "$uri")"
  mkdir -p "$dir_path"
  cp "/wiki/$uri" "$dir_path/"
done

echo "GENERATING RSS FEED"
$TIDDLYWIKI --load /wiki/wiki.html --render "[[$:/plugins/sq/feeds/templates/rss]]" "feed.xml" "text/plain" "$:/core/templates/wikified-tiddler"
mv output/feed.xml /out/feed.xml

echo "ALL DONE"

