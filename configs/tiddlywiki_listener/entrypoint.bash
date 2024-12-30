#!/bin/bash

# Priors - set by podman env or otherwise conventional
# Uncomment for debugging this script
# TMP=~/scratch/wikiscript/tmp
# OUT=~/scratch/wikiscript/out
# WIKI_SRC=~/scratch/wikiscript/wiki

# Comment for debugging this script
TMP=/tmp
OUT=/out
WIKI_SRC=/wiki

# ---

TIDDLYWIKI="tiddlywiki"

OUTPUT=$TMP/NEW
BASE=$OUT/BASE

rm -r $BASE 2>>/dev/null

mkdir $TMP/input
mkdir -p $OUTPUT
mkdir -p $BASE
git --git-dir="$WIKI_SRC" archive master | tar -x -C $TMP/input/

$TIDDLYWIKI --load $TMP/input/phajas-wiki.html --output $TMP/ --render '.' public.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]]:or[tag[phajas]]:or[prefix[$:/phajas]]:except[tag[Private]]' +plugins/tiddlywiki/markdown

/tiddlywiki_strip_public_tag $TMP/public.json
/tiddlywiki_apply_public_fields $TMP/public.json

$TIDDLYWIKI $BASE --init empty 
$TIDDLYWIKI +plugins/tiddlywiki/markdown $BASE --build index

mv $BASE/output/index.html $BASE/

$TIDDLYWIKI --load $BASE/index.html --import $TMP/public.json application/json --output $TMP/ --render "\$:/core/save/all" "$OUTPUT/index.html" "text/plain"

mkdir -p $OUTPUT/static

# HTML representations of individual tiddlers
$TIDDLYWIKI +plugins/tiddlywiki/markdown --load $OUTPUT/index.html --rendertiddlers '[!is[system]]' $:/core/templates/static.tiddler.html $OUTPUT/static text/plain

# CSS
$TIDDLYWIKI --load $OUTPUT/index.html --rendertiddler $:/core/templates/static.template.css $OUTPUT/static/static.css text/plain

# TiddlyWiki likes to take ownership over the directory it operates in, which
# is fine. To help us get the behavior we want with images, move things up a
# level so they're all in `$OUTPUT/` (and nix `$OUTPUT/static`).
mv $OUTPUT/static/* $OUTPUT/
rm -r $OUTPUT/static

$TIDDLYWIKI  --load $TMP/input/phajas-wiki.html --output $TMP/ --render '.' external_assets.json 'text/plain' '$:/core/templates/exporters/JsonFile' 'exportFilter' '[tag[Public]has[_canonical_uri]]'

cat $TMP/external_assets.json | jq -r '.[] | ._canonical_uri' | sed 's/%20/ /g' | while read -r uri; do
  dir_path="$OUTPUT/$(dirname "$uri")"
  mkdir -p "$dir_path"
  cp "$TMP/input/$uri" "$dir_path/"
done

$TIDDLYWIKI +plugins/tiddlywiki/markdown --load $TMP/input/phajas-wiki.html --render "[[$:/plugins/sq/feeds/templates/rss]]" "rss.xml" "text/plain" "$:/core/templates/wikified-tiddler"

# clean up old manifest
while IFS= read -r filepath
do
    # Trim whitespace and expand any potential wildcards
    filepath=$(echo "$filepath" | xargs)
    
    # Skip empty lines
    if [ -z "$filepath" ]; then
        continue
    fi
    
    # Remove file
    rm "$filepath"
    rm -r "$filepath"
done < "$OUT/wiki_manifest.txt"

mv output/rss.xml $OUTPUT/rss.xml

rm -r $BASE

find "$OUTPUT" | sed 's/NEW\///' | sed 's/tmp/out/' | sort > $OUT/wiki_manifest.txt

mv $OUTPUT/* $OUT/

rm -r $OUTPUT

