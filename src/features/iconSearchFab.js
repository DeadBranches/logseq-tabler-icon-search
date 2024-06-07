export function createSearchFAB() {
    const html = String.raw;
    const iconSearchFabHTML = html`
        <md-fab size="small" variant="primary" aria-label="Search" id="icon-search-fab">
            <md-icon slot="icon">&#xeb1c;</md-icon>
        </md-fab>
    `;

    var fabOverlay = document.createElement('div');
    fabOverlay.className = 'fab-container';
    fabOverlay.innerHTML = iconSearchFabHTML;
    document.body.appendChild(fabOverlay);
}

export function handleFabClicks() {
    const iconSearchFab = document.body.querySelector('#icon-search-fab');
    const iconSearchDialog = document.body.querySelector('#icon-search-main-dialog');
    if (!iconSearchFab) { console.log('[iconSearchEventHandlers] Error getting fab element by id.'); return }
    if (!iconSearchDialog) { console.log('[iconSearchEventHandlers] Error getting dialog element by id.'); return }

    iconSearchFab.addEventListener('click', async () => { await iconSearchDialog.show() });
}