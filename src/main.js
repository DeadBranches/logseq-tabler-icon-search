// Frameworks
import Alpine from 'alpinejs';

// Third party components
import '@material/web/all.js';  // This is fine since we tree-shake 
import {styles as typescaleStyles} from '@material/web/typography/md-typescale-styles.js';
document.adoptedStyleSheets.push(typescaleStyles.styleSheet);

// App components
import { createIconSearchFab } from './components/fab/iconSearchFab.js';
import { initializeIconSearchDialog, hideIconSearchDialog } from './components/dialog/iconSearchDialog.js';
import { initializeIconSearchFabEventHandler, initializeIconSearchTabEventHandler } from './subscribers/iconSearchEventHandlers.js';

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {  // window.addEventListener('load', () => {
    createIconSearchFab();
    await initializeIconSearchDialog();
    initializeIconSearchFabEventHandler();
    initializeIconSearchTabEventHandler();
    window.Alpine = Alpine;
    Alpine.start();
});