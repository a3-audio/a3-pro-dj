#!/bin/sh
# Screenshot an SVG or HTML file with headless Firefox (scratch profile). Usage: shot.sh file width height out.png
P="${TMPDIR:-/tmp}/mjlab"
mkdir -p $P/ffprof
f=$(readlink -f "$1")
case "$f" in
  *.svg) printf '<html><body style="margin:0;background:#fcfcfb">%s</body></html>' "$(cat $f)" > $P/shot.html; f=$P/shot.html;;
esac
timeout 90 firefox --headless --no-remote --profile $P/ffprof --window-size $2,$3 --screenshot "$4" "file://$f" >/dev/null 2>&1
