// // Import rollup plugins

// import { rollupPluginHTML as html } from '@web/rollup-plugin-html';
// import {copy} from '@web/rollup-plugin-copy';
// import resolve from '@rollup/plugin-node-resolve';
// import { default as terser } from '@rollup/plugin-terser';
// import minifyHTML from 'rollup-plugin-minify-html-literals';
// import summary from 'rollup-plugin-summary';
// Import rollup plugins
import commonjs from '@rollup/plugin-commonjs';
import { rollupPluginHTML as html } from '@web/rollup-plugin-html';
import { copy } from '@web/rollup-plugin-copy';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';
// import pkgMinifyHTML from 'rollup-plugin-minify-html-literals';
// const minifyHTML = pkgMinifyHTML.default;
import summary from 'rollup-plugin-summary';

export default [
  // First pass for material-components.js
  {
    input: 'src/utils/material-components.js',
    output: {
      file: 'temp/material-components.bundle.js',
      format: 'esm',
    },
    plugins: [
      resolve(),
      commonjs(),
      terser({
        ecma: 2021,
        module: true,
        warnings: true,
        output: { comments: false } // https://stackoverflow.com/questions/60851390/svelte-bundle-js-is-large-full-of-license-comments-even-in-production-mode
      }),
      summary()
    ],
    treeshake: true // Enable tree-shaking
  },
  // Second pass for main.js
  {
    input: 'src/main.js',
    output: {
      file: 'dist/logseq-tabler-icon-search/bundle.js',
      format: 'iife',
      name: 'MyBundle',
      inlineDynamicImports: true
    },
    plugins: [
      // Include the intermediate file without further processing
      {
        name: 'include-material-components',
        resolveId(source) {
          if (source === './utils/material-components.js') {
            return 'temp/material-components.bundle.js';
          }
          return null;
        }
      },
      copy({
        targets: [
          { src: 'src/environments/logseq/custom.js', dest: 'dist/logseq-tabler-icon-search' },
          { src: 'src/styles/*', dest: 'dist/logseq-tabler-icon-search/css' }
          // { src: 'src/', dest: 'dist/logseq-tabler-icon-search/' },
          // { src: 'src/', dest: 'dist/logseq-tabler-icon-search/' },

        ],
        verbose: true
      }),
      summary(),

    ],
    treeshake: false // Disable tree-shaking for this pass
  }
];
