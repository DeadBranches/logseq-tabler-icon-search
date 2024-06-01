/******************************************/
/******************************************/
/*     logseq-tabler-icon-search-ui       */
/******************************************/

/*     project dependancies     */
import './material-components.js'
import Alpine from 'alpinejs';


import { createIconSearchFab } from './iconSearchFab.js';
import { initializeIconSearchDialog, hideIconSearchDialog } from './iconSearchDialog.js';
import { initializeIconSearchFabEventHandler, initializeIconSearchTabEventHandler } from './iconSearchEventHandlers.js';

createIconSearchFab();
document.addEventListener('DOMContentLoaded', async () => {  // window.addEventListener('load', () => {
    await initializeIconSearchDialog();

    initializeIconSearchFabEventHandler();
    initializeIconSearchTabEventHandler();
    window.Alpine = Alpine;
    Alpine.start();
});


// Select your Material Design component
const materialComponent = document.getElementById('icon-search-main-dialog');

// Wait for the component to be fully loaded
materialComponent.addEventListener('load', () => {
  // Access the shadow root of the component
  const shadowRoot = materialComponent.shadowRoot;

  // Create a style element
  const style = document.createElement('style');
  style.textContent = `
  .scrollable .scroller {
    overflow-y: hidden !important;
  }
    .scroller {
      overflow-y: hidden !important;
    }
  `;

  // Append the style to the shadow root
  shadowRoot.appendChild(style);
});


// load css files
// (function() {
//     const cssFile = document.createElement('link');
//     cssFile.rel = 'stylesheet';
//     cssFile.type = 'text/css';
//     cssFile.href = logseqAssetPath() + '/tabler-icon-search-ui/css/main.css';
//     document.head.appendChild(cssFile);
// })();
// (function() {
//     const cssFile = document.createElement('link');
//     cssFile.rel = 'stylesheet';
//     cssFile.type = 'text/css';
//     cssFile.href = logseqAssetPath() + '/tabler-icon-search-ui/css/material-design/light.css';
//     document.head.appendChild(cssFile);
// })();