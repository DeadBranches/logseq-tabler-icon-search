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