let process = 'dev';
// Styles
// import { loadGoogleFonts } from './utils/loadFont.js';
// loadGoogleFonts();
// Conditionally import font-face.css based on the environment
if (process === 'dev') {
  let styleElement = document.createElement('link');
  styleElement.rel = 'stylesheet';
  styleElement.href = './styles/font-face.dev.css';
  document.head.appendChild(styleElement);
} else {
    // Use dynamic asset path depending on platform
    import('./utils/font-face.prod.js');
}

// Import dependencies
import './utils/material-components.js'
import Alpine from 'alpinejs';

// Import components
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