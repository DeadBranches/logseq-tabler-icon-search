
// const iconSearchDialogHTML = `
// <div slot="headline" style="padding: 0px; display: block;">
//     <md-tabs slot="headline" aria-label="Content to view" id="icon-search-primary-tabs">
//         <md-primary-tab aria-controls="icon-search-icons-panel" id="icon-search-icons-tab">Icon search</md-primary-tab>
//         <md-primary-tab aria-controls="icon-search-settings-panel" id="icon-search-settings-tab">Photos</md-primary-tab>
//     </md-tabs>
//     <style>
//         md-tabs::part(divider) {
//             display: none;
//         }
//     </style>

//     <md-linear-progress indeterminate x-show="loading"></md-linear-progress>
// </div>

// <div slot="content" role="tabpanel" aria-labelledby="icons-tab" id="icon-search-icons-panel" class="icon-panel-container">
//                                 <!-- <form slot="content" class="content-container" 
//                             method="dialog" id="icon-search-panel" 
//                             role="tabpanel" aria-labelledby="icon-search-tab"> -->
//     <form class="content-container" method="dialog" id="icon-search-form">


//                                     <!-- <label id="iconSearchTitle">
//                                     <span style="flex: 1;">Icon search</span>
//                                 </label> -->
//         <md-outlined-text-field autofocus label="Icon name" type="search" required x-model="query">
//             <md-icon slot="leading-icon">&#xeb1c;</md-icon>
//         </md-outlined-text-field>
//         <md-text-button form="form-id" x-on:click="fetchResults()">Search</md-text-button>
//     </form>

//     <md-list class="result-container">

//         <template x-for="icon in results" x-bind:key="icon.name">
//             <md-list-item type="button" x-on:click="navigator.clipboard.writeText(icon.glyph); hideOverlay()">
//                 <div slot="headline" x-text="icon.name"></div>
//                 <div slot="supporting-text" x-text="icon.keywords"></div>
//                 <md-icon slot="start" x-html="'&#x' + icon.glyph + ';'" class="search-result"></md-icon>
//             </md-list-item>
//             <md-divider role="separator"></md-divider>
//         </template>
//     </md-list>

// </div>

// <div slot="content" role="tabpanel" aria-labelledby="icon-search-settings-tab" id="icon-search-settings-panel" hidden>
//     hi
// </div>
// `;

export function hideIconSearchDialog() {
    const iconSearch = document.body.querySelector('#icon-search-main-dialog');
    iconSearch.close();
}
// Make the function available for use by AlpineJS instead of having to define it in x-data
window.hideIconSearchDialog = hideIconSearchDialog;

export function initializeIconSearchDialog() {
    return new Promise((resolve, reject) => {

        var iconSearchMainDialog = document.createElement('md-dialog');
        iconSearchMainDialog.id = "icon-search-main-dialog";
        iconSearchMainDialog.setAttribute('class', 'icon-search-overlay');
        iconSearchMainDialog.setAttribute('x-data', `{ 
endpointUrl: 'https://serene.tail0b4c1.ts.net/icon-search/',
query: '',
top_k: 16, 
results: [],
log_open: false,
log_text: [],
Assist: 'lol',
loading: false,

fetchResults() {
    this.loading = ! this.loading;
    this.logMessage('Fetching results...');
    const url = this.endpointUrl + encodeURIComponent(this.query) + '?top_k=' + this.top_k;
    this.logMessage('Endpoint url: ' + url);

    fetch(url)
    .then(response => response.json())
    .then(data => {
        this.loading = ! this.loading;
        this.results = data.result;

        this.logMessage('Data recieved successfully.');
        this.logMessage(JSON.stringify(data.result, null, 2));
        this.logMessage('Results rendered.');
    })
    .catch(error => {
        this.loading = ! this.loading;
        
        this.logMessage('Error fetching results.');
        this.logMessage('Content origin: ' + window.location.origin);
        console.log('Content origin: ' + window.location.origin);
    });
  },
//   hideOverlay() {
//     const iconSearch = document.body.querySelector('#icon-search-main-dialog');
//     iconSearch.close();
// },
  logMessage(content) {
    this.log_text.push(content);
    this.$nextTick(() => {
        const logContainer = this.$refs.logContainer;
        //logContainer.scrollTop = logContainer.scrollHeight;
      });
  },
}`);

        fetch('../resources/html/md-dialog.html')
            .then(response => response.text())
            .then(htmlString => {
                iconSearchMainDialog.innerHTML = htmlString;

                document.body.appendChild(iconSearchMainDialog);
                resolve();
            })
            .catch(error => {
                console.error('Error loading HTML:', error);
                reject(error);
            });

    });
}