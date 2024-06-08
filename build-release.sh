#!/bin/bash

mkdir release
mkdir release/assets
mkdir release/assets/logseq-tabler-icon-search
mkdir release/assets/logseq-tabler-icon-search/font
mkdir release/assets/logseq-tabler-icon-search/js

echo "Resolving material design components and creating main.js"
npx rollup -c

echo "Copying logseq custom.js"
cp src/environments/logseq/* release

echo "Copying font assets"
cp node_modules/@tabler/icons-webfont/dist/fonts/tabler-icons.* release/assets/logseq-tabler-icon-search/font

echo "Copying script assets"
cp node_modules/alpinejs/dist/cdn.min.js release/assets/logseq-tabler-icon-search/js/alpine.min.js
cp node_modules/@alpinejs/persist/dist/cdn.js release/assets/logseq-tabler-icon-search/js/alpine.persist.js

echo "Done."

