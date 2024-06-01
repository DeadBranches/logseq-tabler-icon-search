#!/bin/bash
nvm install 20.14.0
nvm use 20.14.0

#npm init
npm install --save-dev @web/dev-server rollup @web/rollup-plugin-html @web/rollup-plugin-copy @rollup/plugin-node-resolve @rollup/plugin-terser rollup-plugin-minify-html-literals rollup-plugin-summary
npm install @material/web @tabler/icons @tabler/icons-webfont