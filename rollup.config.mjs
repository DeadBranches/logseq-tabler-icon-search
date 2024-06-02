// // Import rollup plugins

// import { rollupPluginHTML as html } from '@web/rollup-plugin-html';
// import {copy} from '@web/rollup-plugin-copy';
// import resolve from '@rollup/plugin-node-resolve';
// import { default as terser } from '@rollup/plugin-terser';
// import minifyHTML from 'rollup-plugin-minify-html-literals';
// import summary from 'rollup-plugin-summary';
// Import rollup plugins

import { rollupPluginHTML as html } from '@web/rollup-plugin-html';
import { copy } from '@web/rollup-plugin-copy';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';
// import pkgMinifyHTML from 'rollup-plugin-minify-html-literals';
// const minifyHTML = pkgMinifyHTML.default;
import summary from 'rollup-plugin-summary';


export default [
  {
    input: 'src/environments/logseq/custom.js',
    output: {
      file: 'dist/custom.js',
      format: 'iife'
    },
    plugins: []
  },
  {
    input: 'src/resources/js/material-web-components.js',
    plugins: [
      // Entry point for application build; can specify a glob to build multiple
      // HTML files for non-SPA app
      // html({
      //   input: 'index.html',
      // }),

      // Resolve bare module specifiers to relative paths
      resolve(),

      // Minify HTML template literals
      // minifyHTML(),

      // Minify JS

      terser({
        ecma: 2021,
        module: true,
        warnings: true,
        output: { comments: false } // https://stackoverflow.com/questions/60851390/svelte-bundle-js-is-large-full-of-license-comments-even-in-production-mode
      }),
      // Print bundle summary
      summary(),
      // Optional: copy any static assets to build directory

      // copy({
      //   patterns: ['images/**/*'],
      // }),
    ],
    output: {
      dir: 'build',
    },
    preserveEntrySignatures: 'strict',
  },
];