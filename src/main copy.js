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

let stylesheet = document.createElement('style');
stylesheet.innerHTML = `
md-dialog.icon-search#icon-search-main-dialog {
  height: 70vh;
  width: 70vh;
}

header.icon-search {
  height: 10vh;
  /* [slot="headline"] */
  padding: 0px;
  display: block;
}
md-tabs.icon-search::part(divider) {
  display: none;
}

#icon-search-icons-panel {
  height: 60vh;
  overflow: hidden;
}
.horizontally-fill {
  padding-left: 0 !important;
  padding-right: 0 !important;
}
#icon-search-query md-icon {
  cursor: pointer;
}

#icon-search-results-container {
  height: 70%;
  margin-top: 1rem; /* Space between the search form and results */
  overflow-y: scroll;
  /* overflow-y: auto; also seems to work?*/
}

.hidden-scrollbar {
  -webkit-scrollbar {
    display: none;
  }
  scrollbar-width: none;
}

/* Attempt at grid-based list */
.grid-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 5px;
}

.top-align-content {
  /* align = vertical */
  display: flex;
  align-items: start;
}
.center-align-content {
  /* align = vertical */
  display: flex;
  align-items: center;
}
.center-content {
  /* justify = horizontal */
  display: flex;
  justify-content: center;
  text-align: center;
}
.center-self {
  margin: auto;
}
.block {
  display: block;
}


/*  */

/* Settings pane */
.icon-search-settings-row {
  display: flex;
  align-items: center;
  /* This will vertically center the content in the row */
  margin-bottom: 20px;
  /* Space between rows */
}

.icon-search-settings-icon-column {
  flex: 0 0 auto;
  /* Do not grow or shrink */
  width: 50px;
  /* Adjust as needed */
  text-align: center;
  /* Center the icon horizontally */
  margin: 0px;
}

.icon-search-settings-content-column {
  flex: 1;
  /* Take up the remaining space */
  display: flex;
  flex-direction: column;
  /* Stack label and slider on top of each other */
  align-items: flex-start;
  /* Align content to the start of the column */
}

.icon-search-settings-content-column label,
.icon-search-settings-content-column md-slider {
  width: 100%;
  /* Full width of the column */
}

.fab-container {
  z-index: 1;
  position: fixed;
  right: 5vh;
  bottom: 20vw;
}

md-dialog {
  overflow: hidden;
}

.fab-container {
  z-index: 2;
  position: fixed;
  right: 16px;
  bottom: 16px;
}
md-icon {
  --md-icon-font: 'better-tabler-icons';
  /* font-family: "better-tabler-icons"; */
  /* display: inline; */
}


md-icon.large {
  width: 40px;
  height: 40px;
  font-size: 40px;
  /* line-height */
  /* margin: 0; */
  /* https://github.com/angular/components/issues/4422#issuecomment-428303380 */
}

/* md-icon.search-result {
  width: 40px;
  height: 40px;
  font-size: 40px; */
  /* line-height */
  /* margin: 0; */
  /* https://github.com/angular/components/issues/4422#issuecomment-428303380 */
/* } */

`;
document.head.appendChild(stylesheet);


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