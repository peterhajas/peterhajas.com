#!/bin/bash

echo "PREPARING"
# TIDDLYWIKI="tiddlywiki +plugins/tiddlywiki/markdown --verbose"
TIDDLYWIKI="tiddlywiki +plugins/tiddlywiki/markdown"
OUTPUT=/out/NEW
BASE=/out/BASE

mkdir /tmp/input
mkdir -p $OUTPUT
mkdir -p $BASE
git --git-dir=/wiki archive master | tar -x -C /tmp/input/

echo "CLEANING UP"
rm /out/*
rm -r /out/*

echo "EXPORTING"
$TIDDLYWIKI --load /tmp/input/phajas-wiki.html --output /tmp/ --render '.' public.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]]:or[tag[phajas]]:or[prefix[$:/phajas]]:except[tag[Private]]'

echo "STRIPPING PUBLIC TAGS"
/tiddlywiki_strip_public_tag /tmp/public.json

echo "APPLYING PUBLIC FIELDs"
/tiddlywiki_apply_public_fields /tmp/public.json

echo "CREAETING NEW BASE WIKI"
$TIDDLYWIKI $BASE --init empty
$TIDDLYWIKI $BASE --build index

echo "IMPORTING INTO BASE WIKI"
$TIDDLYWIKI --load $BASE/output/index.html --import /tmp/public.json application/json --output /tmp/ --render "\$:/core/save/all" "$OUTPUT/index.html" "text/plain"

echo "GENERATING STATIC VARIANT"
mkdir -p $OUTPUT/static

# HTML representations of individual tiddlers
$TIDDLYWIKI --load $OUTPUT/index.html --rendertiddlers '[!is[system]]' $:/core/templates/static.tiddler.html $OUTPUT/static text/plain

# CSS
$TIDDLYWIKI --load $OUTPUT/index.html --rendertiddler $:/core/templates/static.template.css $OUTPUT/static/static.css text/plain

# TiddlyWiki likes to take ownership over the directory it operates in, which
# is fine. To help us get the behavior we want with images, move things up a
# level so they're all in `$OUTPUT/` (and nix `$OUTPUT/static`).
mv $OUTPUT/static/* $OUTPUT/
rm -r $OUTPUT/static

echo "GRABBING PUBLIC EXTERNAL ASSETS"
$TIDDLYWIKI --load /tmp/input/phajas-wiki.html --output /tmp/ --render '.' external_assets.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]has[_canonical_uri]]'

cat /tmp/external_assets.json | jq -r '.[] | ._canonical_uri' | sed 's/%20/ /g' | while read -r uri; do
  dir_path="$OUTPUT/$(dirname "$uri")"
  mkdir -p "$dir_path"
  cp "/tmp/input/$uri" "$dir_path/"
done

echo "GENERATING RSS FEED"
$TIDDLYWIKI --load /tmp/input/phajas-wiki.html --render "[[$:/plugins/sq/feeds/templates/rss]]" "feed.xml" "text/plain" "$:/core/templates/wikified-tiddler"
mv output/feed.xml $OUTPUT/feed.xml

echo "CLEANING UP"
rm /out/*
mv $OUTPUT/* /out/

echo "ALL DONE"

