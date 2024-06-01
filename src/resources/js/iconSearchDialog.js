export function hideIconSearchDialog() {
    const iconSearch = document.body.querySelector('#icon-search-main-dialog');
    iconSearch.close();
}
// Make the function available for use by AlpineJS instead of having to define it in x-data
window.hideIconSearchDialog = hideIconSearchDialog;

export function initializeIconSearchDialog() {
    return new Promise((resolve, reject) => {

        fetch('../resources/html/md-dialog.html')
            .then(response => response.text())
            .then(htmlString => {
                document.body.insertAdjacentHTML('beforeend', htmlString);
                resolve();
            })
            .catch(error => {
                console.error('Error loading HTML:', error);
                reject(error);
            });

    });
}