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
      dir: 'dist/logseq-tabler-icon-search',
      format: 'iife',
      name: 'IconSearch',
      sourcemap: true
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
      copy([
          { src: 'src/assets/font/*', dest: 'dist/logseq-tabler-icon-search/assets' },
          { src: 'src/environments/logseq', dest: 'dist/logseq-tabler-icon-search'}
        ]
      ),
      postcss({
        plugins: [],
        inject: false,
        extract: true,
        sourceMap: true,
        minimize: false
    }),
      summary()
    ],
    treeshake: true // Enable tree-shaking
  }
];
