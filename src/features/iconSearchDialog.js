export function hideIconSearchDialog() {
    const iconSearch = document.body.querySelector('#icon-search-main-dialog');
    iconSearch.close();
}
// Make the function available for use by AlpineJS instead of having to define it in x-data
window.hideIconSearchDialog = hideIconSearchDialog;

export function initializeIconSearchDialog() {
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
};


