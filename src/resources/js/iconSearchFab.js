const iconSearchFabHTML = `
    <md-fab size="small" variant="primary" aria-label="Search" id="icon-search-fab">
        <md-icon slot="icon">&#xeb1c;</md-icon>
    </md-fab>

`;

export function createIconSearchFab() {
    var fabOverlay = document.createElement('div');
    fabOverlay.className = 'fab-container';
    fabOverlay.innerHTML = iconSearchFabHTML;
    document.body.appendChild(fabOverlay);
}