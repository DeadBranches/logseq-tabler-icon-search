export function initializeIconSearchFabEventHandler() {
    const iconSearchFab = document.body.querySelector('#icon-search-fab');
    const iconSearchDialog = document.body.querySelector('#icon-search-main-dialog');
    if (!iconSearchFab) { console.log('[iconSearchEventHandlers] Error getting fab element by id.'); return }
    if (!iconSearchDialog) { console.log('[iconSearchEventHandlers] Error getting dialog element by id.'); return }

    iconSearchFab.addEventListener('click', async () => { await iconSearchDialog.show() });
}

export function initializeIconSearchTabEventHandler() {
    const iconSearchPrimaryTabsElement = document.getElementById('icon-search-primary-tabs');
    const iconSearchIconsPanel = document.getElementById('icon-search-icons-panel');
    const iconSearchSettingsPanel = document.getElementById('icon-search-settings-panel');

    if (!iconSearchPrimaryTabsElement) { console.log('[iconSearchEventHandlers] Error getting primary tab elemenmt.'); return;  }
    if (!iconSearchIconsPanel) {  console.log('[iconSearchEventHandlers] Error getting icon panel element.'); return  }
    if (!iconSearchSettingsPanel) { console.log('[iconSearchEventHandlers] Error getting settings panel element.'); return  }

    iconSearchPrimaryTabsElement.addEventListener('change', function (event) {
        var target = event.target;

        // Check if the activeTabIndex property exists on the target
        if ('activeTabIndex' in target) {
            // Assuming the tabs start at index 0
            if (target.activeTabIndex === 0) {
                iconSearchIconsPanel.removeAttribute('hidden');
                iconSearchSettingsPanel.setAttribute('hidden', 'hidden');
            } else if (target.activeTabIndex === 1) {
                iconSearchIconsPanel.setAttribute('hidden', 'hidden');
                iconSearchSettingsPanel.removeAttribute('hidden');
            }
        }
    });
}