#!/bin/bash

echo "PREPARING"
TIDDLYWIKI="tiddlywiki"

OUTPUT=/tmp/NEW
BASE=/out/BASE

rm -r $BASE 2>>/dev/null

mkdir /tmp/input
mkdir -p $OUTPUT
mkdir -p $BASE
git --git-dir=/wiki archive master | tar -x -C /tmp/input/

$TIDDLYWIKI --load /tmp/input/phajas-wiki.html --output /tmp/ --render '.' public.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]]:or[tag[phajas]]:or[prefix[$:/phajas]]:except[tag[Private]]'

/tiddlywiki_strip_public_tag /tmp/public.json

/tiddlywiki_apply_public_fields /tmp/public.json

$TIDDLYWIKI /out/BASE --init empty
$TIDDLYWIKI /out/BASE --build index

ls /out/BASE

mv $BASE/output/index.html $BASE/

ls $BASE

$TIDDLYWIKI --load $BASE/index.html --import /tmp/public.json application/json --output /tmp/ --render "\$:/core/save/all" "$OUTPUT/index.html" "text/plain"

ls $OUTPUT

mkdir -p $OUTPUT/static

# HTML representations of individual tiddlers
$TIDDLYWIKI +plugins/tiddlywiki/markdown --verbose --load $OUTPUT/index.html --rendertiddlers '[!is[system]]' $:/core/templates/static.tiddler.html $OUTPUT/static text/plain

# CSS
$TIDDLYWIKI --load $OUTPUT/index.html --rendertiddler $:/core/templates/static.template.css $OUTPUT/static/static.css text/plain

# TiddlyWiki likes to take ownership over the directory it operates in, which
# is fine. To help us get the behavior we want with images, move things up a
# level so they're all in `$OUTPUT/` (and nix `$OUTPUT/static`).
mv $OUTPUT/static/* $OUTPUT/
# rm -r $OUTPUT/static

$TIDDLYWIKI  --load /tmp/input/phajas-wiki.html --output /tmp/ --render '.' external_assets.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]has[_canonical_uri]]'

cat /tmp/external_assets.json | jq -r '.[] | ._canonical_uri' | sed 's/%20/ /g' | while read -r uri; do
  dir_path="$OUTPUT/$(dirname "$uri")"
  mkdir -p "$dir_path"
  cp "/tmp/input/$uri" "$dir_path/"
done

$TIDDLYWIKI --load /tmp/input/phajas-wiki.html --render "[[$:/plugins/sq/feeds/templates/rss]]" "rss.xml" "text/plain" "$:/core/templates/wikified-tiddler" +plugins/tiddlywiki/markdown --verbose
mv output/rss.xml $OUTPUT/rss.xml

rm /out/*
rm -r /out/*
rm -r /out/BASE
mv --force /tmp/NEW/* /out/

