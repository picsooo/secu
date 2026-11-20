#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 build.py
OUT=../public
javascript-obfuscator p.src.js --output $OUT/assets/p.js --compact true --control-flow-flattening true --string-array true --string-array-encoding base64 --self-defending true >/dev/null
cleancss -o $OUT/assets/site.css $OUT/assets/site.css
find $OUT -name '*.html' -print0 | while IFS= read -r -d '' f; do
  html-minifier-terser --collapse-whitespace --remove-comments --minify-css true --minify-js true -o "$f" "$f"
done
cat > ../vercel.json <<'J'
{"outputDirectory":"public","buildCommand":"","headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow"},{"key":"X-Frame-Options","value":"DENY"}]}]}
J
echo built
