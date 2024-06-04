// Frameworks
import Alpine from 'alpinejs';
import persist from '@alpinejs/persist';

// Third party components
import '@material/web/all.js';  // This is fine since we tree-shake 
import { styles as typescaleStyles } from '@material/web/typography/md-typescale-styles.js';
document.adoptedStyleSheets.push(typescaleStyles.styleSheet);

// App components
import { createIconSearchFab } from './features/iconSearchFab.js';
import { initializeIconSearchDialog, hideIconSearchDialog } from './features/iconSearchDialog.js';
import { initializeIconSearchFabEventHandler, initializeIconSearchTabEventHandler } from './subscribers/iconSearchEventHandlers.js';

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {  // window.addEventListener('load', () => {
  createIconSearchFab();
  await initializeIconSearchDialog();
  initializeIconSearchFabEventHandler();
  initializeIconSearchTabEventHandler();
  window.Alpine = Alpine;
  Alpine.plugin(persist)
  Alpine.start();

});

import './styles/md-dialog.css';
import './styles/md-fab.css';
import './styles/md-icon.css';
import './styles/material-design/light.css';
import './styles/tabler-icons-font.css';