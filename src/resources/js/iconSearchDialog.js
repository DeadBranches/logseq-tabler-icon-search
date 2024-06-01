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