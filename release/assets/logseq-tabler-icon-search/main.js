import './node_modules/@material/web/button/elevated-button.js';
import './node_modules/@material/web/button/filled-button.js';
import './node_modules/@material/web/button/filled-tonal-button.js';
import './node_modules/@material/web/button/outlined-button.js';
import './node_modules/@material/web/button/text-button.js';
import './node_modules/@material/web/checkbox/checkbox.js';
import './node_modules/@material/web/chips/assist-chip.js';
import './node_modules/@material/web/chips/chip-set.js';
import './node_modules/@material/web/chips/filter-chip.js';
import './node_modules/@material/web/chips/input-chip.js';
import './node_modules/@material/web/chips/suggestion-chip.js';
import './node_modules/@material/web/dialog/dialog.js';
import './node_modules/@material/web/divider/divider.js';
import './node_modules/@material/web/elevation/elevation.js';
import './node_modules/@material/web/fab/branded-fab.js';
import './node_modules/@material/web/fab/fab.js';
import './node_modules/@material/web/field/filled-field.js';
import './node_modules/@material/web/field/outlined-field.js';
import './node_modules/@material/web/focus/md-focus-ring.js';
import './node_modules/@material/web/icon/icon.js';
import './node_modules/@material/web/iconbutton/filled-icon-button.js';
import './node_modules/@material/web/iconbutton/filled-tonal-icon-button.js';
import './node_modules/@material/web/iconbutton/icon-button.js';
import './node_modules/@material/web/iconbutton/outlined-icon-button.js';
import './node_modules/@material/web/list/list.js';
import './node_modules/@material/web/list/list-item.js';
import './node_modules/@material/web/menu/menu.js';
import './node_modules/@material/web/menu/menu-item.js';
import './node_modules/@material/web/menu/sub-menu.js';
import './node_modules/@material/web/progress/circular-progress.js';
import './node_modules/@material/web/progress/linear-progress.js';
import './node_modules/@material/web/radio/radio.js';
import './node_modules/@material/web/ripple/ripple.js';
import './node_modules/@material/web/select/filled-select.js';
import './node_modules/@material/web/select/outlined-select.js';
import './node_modules/@material/web/select/select-option.js';
import './node_modules/@material/web/slider/slider.js';
import './node_modules/@material/web/switch/switch.js';
import './node_modules/@material/web/tabs/primary-tab.js';
import './node_modules/@material/web/tabs/secondary-tab.js';
import './node_modules/@material/web/tabs/tabs.js';
import './node_modules/@material/web/textfield/filled-text-field.js';
import './node_modules/@material/web/textfield/outlined-text-field.js';
import { styles } from './node_modules/@material/web/typography/md-typescale-styles.js';

// Third party components

document.adoptedStyleSheets.push(styles.styleSheet);


// Tabler icons
(function () {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        @font-face {
        font-family: "better-tabler-icons";
        font-style: normal;
        font-weight: 400;
        src: url("${logseqAssetPath()}/logseq-tabler-icon-search/font/tabler-icons.woff2") format("woff2"),
                url("${logseqAssetPath()}/logseq-tabler-icon-search/font/tabler-icons.woff") format("woff"),
                url("${logseqAssetPath()}/logseq-tabler-icon-search/font/tabler-icons.ttf") format("truetype"); // Corrected the file extension
        }
    `;
    document.head.appendChild(styleElement);

})();


// Third party frameworks

(function () {
    // AlpineJS core
    //  "A rugged, minimal framework for composing JavaScript behavior in your markup. "
    //  source: https://github.com/alpinejs/alpine
    //  documentation: https://alpinejs.dev/start-here
    let alpinePersist = document.createElement('script');
    alpinePersist.src = `${logseqAssetPath()}/logseq-tabler-icon-search/js/alpine.persist.js`;
    alpinePersist.defer = true;
    document.head.appendChild(alpinePersist);
    
    // AlpineJS persist
    //  "Alpine's Persist plugin allows you to persist Alpine state across page loads."
    //  documentation: https://alpinejs.dev/plugins/persist
    let alpineScript = document.createElement('script');
    alpineScript.src = `${logseqAssetPath()}/logseq-tabler-icon-search/js/alpine.min.js`;
    alpineScript.defer = true;
    document.head.appendChild(alpineScript);

    let alpineVersion;
    try {
        alpineVersion = JSON.stringify(window.Alpine);
        logseq.api.show_msg("Alpine loaded", "success");
    } catch (err) {
        logseq.api.show_msg("Alpine failed to load", "error");
    }

})();



// logseq-tabler-icon-search
(function () {
    function createSearchFAB() {
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
    

    function handleFabClicks() {
        const iconSearchFab = document.body.querySelector('#icon-search-fab');
        const iconSearchDialog = document.body.querySelector('#icon-search-main-dialog');
        if (!iconSearchFab) { console.log('[iconSearchEventHandlers] Error getting fab element by id.'); return }
        if (!iconSearchDialog) { console.log('[iconSearchEventHandlers] Error getting dialog element by id.'); return }
        iconSearchFab.addEventListener('click', async () => { await iconSearchDialog.show(); });
    }


    function hideDialog() {
        const iconSearch = document.body.querySelector('#icon-search-main-dialog');
        iconSearch.close();
    }
    // Make the function available for use by AlpineJS instead of having to define it in x-data
    

    function createDialog() {
        const html = String.raw;
        const iconSearchDialog = html`
        <md-dialog id="icon-search-main-dialog" class="icon-search" x-data="{
            // Settings
            endpointUrl: $persist('https://serene.tail0b4c1.ts.net/icon-search/'),
            top_k: $persist(16),
            negative_queries: $persist(['']),
            // State
            loading: false,
            log_text: [],
    
                logMessage(content) {
                this.log_text.push(content);
                this.$nextTick(() => {
                    const logContainer = this.$refs.logContainer;
                    //logContainer.scrollTop = logContainer.scrollHeight;
                    });
                },
            }">
    
            <header slot="headline" class="icon-search">
                <md-tabs id="icon-search-primary-tabs" aria-label="Content to view" class="icon-search">
                    <md-primary-tab id="icon-search-icons-tab" aria-controls="icon-search-icons-panel">
                        Icon search
                    </md-primary-tab>
                    <md-primary-tab id="icon-search-settings-tab" aria-controls="icon-search-settings-panel">
                        Settings
                    </md-primary-tab>
                </md-tabs>
    
                <md-linear-progress indeterminate x-show="loading"></md-linear-progress>
            </header>
    
            <main slot="content" id="icon-search-icons-panel" role="tabpanel" aria-labelledby="icons-tab"
                class="icon-search horizontally-fill" 
                x-data="{        
                // Search
                query: '',
                results: [],
    
                fetchResults() {
                    loading = ! loading;
                    $refs.iconSearchQuery.blur(); // hide keyboard
                    const query_parameters = [];
                    query_parameters.push('top_k=' + top_k);
                    if (negative_queries && negative_queries.length) {  // Check if empty
                        const negative_query_string = negative_queries.map(query => 'negative_search_strings=' + encodeURIComponent(query)).join('&')
                        query_parameters.push(negative_query_string)
                    }
                    const url = endpointUrl + encodeURIComponent(this.query) + '?' + query_parameters.join('&');
    
                    //const negative_query_search = negative_queries ? negative_queries.map(query => 'negative_queries[]=' + encodeURIComponent(query).join('&') : [''];
                    logMessage('Fetching results from endpoint ' + url);
    
                    fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        this.results = data.result;
                        loading = ! loading;
                        $refs.iconSearchQuery.blur(); // hide keyboard
                        logMessage('Data recieved');
                    })
                    .catch(error => {
                        loading = ! loading;
                        logMessage('Error fetching results.\n\nContent origin: ' + window.location.origin);
                        console.log('Content origin: ' + window.location.origin);
                    });
                }
            }">
                <section class="center-content">
                    <form id="icon-search-form" method="dialog">
                        <md-filled-text-field id="icon-search-query" x-ref="iconSearchQuery" label="Icon name" autofocus
                            required x-on:focus="$refs.iconSearchQuery.select()" x-on:keyup.enter="fetchResults"
                            x-model="query">
                            <md-icon-button x-ref="searchQueryButton" slot="trailing-icon" x-on:click.prevent="fetchResults">
                                <md-icon>&#xeb1c;</md-icon>
                            </md-icon-button>
                        </md-filled-text-field>
                    </form>
                </section>
    
                <md-list id="icon-search-results-container" class="grid-3col hidden-scrollbar">
                    <template x-for="icon in results" x-bind:key="icon.name">
                        <md-list-item type="button"
                            x-on:click="navigator.clipboard.writeText(icon.glyph); hideIconSearchDialog()"
                            class="center-content top-align-content">
    
                            <md-icon slot="headline" x-html="'&#x' + icon.glyph + ';'" class="block center-self large"
                                style="margin-bottom: 1rem;"></md-icon>
    
                            <span slot="supporting-text" x-html="icon.name.replace(/-./g, function(match) {
                                return match.length === 2 ? ' ' + match[1] : '<br>';
                            })"></span>
                            <!-- Replace hyphens with linebreaks, unless the next word is a single letter, in which case replace with a space. https://sl.bing.net/boC9kFkW5KK -->
    
                        </md-list-item>
                        <md-divider role="separator"></md-divider>
                    </template>
                </md-list>
            </main>
    
            <!-- settings panel -->
            <main id="icon-search-settings-panel" slot="content" role="tabpanel" aria-labelledby="icon-search-settings-tab"
                hidden x-data="{ index: 0 }">
                
                <!-- search result quantity -->
                <div class="icon-search-settings-row">
                    <div class="icon-search-settings-content-column">
                        <label for="result_quantity">Search results</label>
                        <md-slider id="result_quantity" min="20" max="200" value="40" step="10"
                            x-model.number.debounce.500ms="top_k" labeled></md-slider>
                    </div>
                    <figure class="icon-search-settings-icon-column">
                        <md-icon>&#xf3f3;</md-icon>
                    </figure>
                </div>
    
                <!-- Endpoint address -->
                <div class="icon-search-settings-row center-content">
                    <div class="icon-search-settings-content-column center-content">
                        <md-filled-text-field label="Endpoint address" type="url" placeholder="http://" x-model="endpointUrl"
                            class="center-self">
                        </md-filled-text-field>
                    </div>
                    <span class="icon-search-settings-icon-column"></span>
                </div>
    
                <!-- Negative queries -->
                <template x-for="(negative_query, index) in negative_queries" x-bind:key="index">
                    <div class="icon-search-settings-row center-content">
                        <md-filled-text-field label="Negative query" x-model="negative_queries[index]"
                            class="icon-search-settings-content-column">
                        </md-filled-text-field>
                        <md-icon-button x-on:click="negative_queries.splice(index, 1)" class="icon-search-settings-icon-column">
                            <md-icon>&#xeaf2;</md-icon>
                        </md-icon-button>
                    </div>
                </template>
                <div class="icon-search-settings-row center-content">
                    <div class="icon-search-settings-content-column">
                    </div>
                    <md-icon-button x-on:click="negative_queries.push('')" class="icon-search-settings-icon-column">
                        <md-icon>&#xea69;</md-icon> <!-- This should be an 'add' icon -->
                    </md-icon-button>
                </div>
    
            </main>
        </md-dialog>
        `;
    
        document.body.insertAdjacentHTML('beforeend', iconSearchDialog);
    }    
    
    function listenForTabEvents() {
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
    

    function insertMdDialogStyles() {
        const css = String.raw;
        const mdDialog = css`
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
          
            md-dialog {
                overflow: hidden;
            }
        `;

        let stylesheet = document.createElement('style');
        stylesheet.innerHTML = mdDialog;
        document.head.appendChild(stylesheet);
    }


    function insertMdFabStyles() {
        const css = String.raw;
        const mdFab = css`
            .fab-container {
                z-index: 1;
                position: fixed;
                right: 5vh;
                bottom: 20vw;
            }
            @media screen and (max-width: 360px) {
                .fab-container {
                    right: 15vh;
                    bottom: 40vw;
                }
            }
        `;
        let stylesheet = document.createElement('style');
        stylesheet.innerHTML = mdFab;
        document.head.appendChild(stylesheet);
    }
    

    function insertMdIconStyles() {
        const css = String.raw;
        const mdIcon = css`
            
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
            
        `;
        let stylesheet = document.createElement('style');
        stylesheet.innerHTML = mdIcon;
        document.head.appendChild(stylesheet);
    
    }

    // Initialize the application
    window.hideIconSearchDialog = hideDialog;

    insertMdIconStyles();
    insertMdFabStyles();
    insertMdDialogStyles();

    createSearchFAB();
    createDialog();
    handleFabClicks();
    listenForTabEvents();

})();
