#!/bin/sh
# Render SVGs to PNG for a look: CSS var() fallbacks replaced by their hex.
OUT="${TMPDIR:-/tmp}/mjlab"
mkdir -p $OUT
for f in "$@"; do
  b=$(basename $f .svg)
  sed -E 's/var\(--[a-z0-9]+,(#[0-9a-fA-F]+)\)/\1/g' $f  > $OUT/$b.svg
  magick -background '#fcfcfb' -density 140 $OUT/$b.svg $OUT/$b.png
done
