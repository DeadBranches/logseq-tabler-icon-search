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
    input: 'src/index.html',
    output: {
      // file: 'dist/logseq-tabler-icon-search/bundle.js',
      dir: 'dist/logseq-tabler-icon-search',
      // format: 'iife',
      name: 'IconSearch',
      // sourcemap: true
    },

    treeshake: true,
    
    plugins: [
      // postcss({
      //   extensions: ['.css'],
      //   minimize: false,
      //   sourceMap: true
      // }),
            copy(
        [
          { 
            src: 'src/assets/font', 
            dest: 'dist/logseq-tabler-icon-search/assets' 
          },
          {
            src: 'src/styles',
            dest: 'dist/logseq-tabler-icon-search'
          },
          { 
            src: 'src/environments/logseq', 
            dest: 'dist/logseq-tabler-icon-search'
          }
        ]
      ),
      resolve(),
      // commonjs(),
      // terser({
      //   compress: false,
      //   mangle: false,
      //   ecma: 2021,
      //   module: true,
      //   warnings: true,
      //   output: { comments: false } 
      // }),


      html(),
      summary()
    ],
  }
]
