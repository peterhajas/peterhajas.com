#!/bin/bash

echo "CLEANING UP"
rm /out/*
rm -r /out/*

echo "EXPORTING"
tiddlywiki --verbose --load /wiki/wiki.html --output /tmp/ --render '.' public.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]]:or[tag[phajas]]:or[prefix[$:/phajas]]:except[tag[Private]]'

echo "STRIPPING PUBLIC TAGS"
/tiddlywiki_strip_public_tag /tmp/public.json

echo "IMPORTING INTO BASE WIKI"
tiddlywiki --verbose --load /base.html --import /tmp/public.json application/json --output /tmp/ --render "\$:/core/save/all" "/out/out.html" "text/plain"

echo "GRABBING PUBLIC EXTERNAL ASSETS"
tiddlywiki --verbose --load /wiki/wiki.html --output /tmp/ --render '.' external_assets.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]has[_canonical_uri]]'

cat /tmp/external_assets.json | jq -r '.[] | ._canonical_uri' | sed 's/%20/ /g' | while read -r uri; do
  dir_path="/out/$(dirname "$uri")"
  mkdir -p "$dir_path"
  cp "/wiki/$uri" "$dir_path/"
done

echo "GENERATING RSS FEED"
tiddlywiki +plugins/tiddlywiki/markdown --load /wiki/wiki.html --render "[[$:/plugins/sq/feeds/templates/rss]]" "feed.xml" "text/plain" "$:/core/templates/wikified-tiddler"
mv output/feed.xml /out/feed.xml

echo "ALL DONE"

