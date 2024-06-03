// Framework dependancies
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