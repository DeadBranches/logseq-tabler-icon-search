// Frameworks
import Alpine from 'alpinejs';
import persist from '@alpinejs/persist';

// Third party components
import '@material/web/all.js';  // This is fine since we tree-shake 
import { styles as typescaleStyles } from '@material/web/typography/md-typescale-styles.js';
document.adoptedStyleSheets.push(typescaleStyles.styleSheet);

import './styles/md-dialog.css';
import './styles/md-fab.css';
import './styles/md-icon.css';
import './styles/material-design/light.css';
// import './styles/tabler-icons-font.css';

// let stylesheet = document.createElement('link');
// stylesheet.rel = 'stylesheet';
// stylesheet.href = 'assets/styles/styles.css';
// document.head.appendChild(stylesheet);


// App components
import { createSearchFAB, handleFabClicks } from './features/iconSearchFab.js';
import { createDialog, hideDialog, listenForTabEvents } from './features/iconSearchDialog.js';


// Initialize the application
document.addEventListener('DOMContentLoaded', () => {  

  createSearchFAB();
  createDialog();
  handleFabClicks();
  listenForTabEvents();
  
  window.Alpine = Alpine;
  Alpine.plugin(persist)
  Alpine.start();
});