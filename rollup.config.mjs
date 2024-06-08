// Import rollup plugins
import commonjs from '@rollup/plugin-commonjs';
import { rollupPluginHTML as html } from '@web/rollup-plugin-html';
// import { copy } from '@web/rollup-plugin-copy';
import { copy } from 'vite-plugin-copy';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';
import postcss from 'rollup-plugin-postcss';
import url from '@rollup/plugin-url';
import summary from 'rollup-plugin-summary';

export default [
  // First pass for material-components.js
  {
    input: 'src/main.js',
    output: {
      // file: 'dist/logseq-tabler-icon-search/bundle.js',
      dir: 'release/assets/logseq-tabler-icon-search',
      // format: 'iife',
      format: 'esm',
      name: 'IconSearch',
      preserveModules: true,
      preserveModulesRoot: 'src',
    },

    plugins: [
      resolve(),
      summary()
    ],
  }
]
