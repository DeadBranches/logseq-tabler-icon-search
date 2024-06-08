class AssetPathManager {
    /**
     * Manages asset paths for different platforms within an electron application.
     *
     * This class implements a singleton pattern to ensure that only one instance
     * manages the asset paths throughout the application. It provides a method to
     * retrieve the correct asset path based on the user's operating system, which
     * is determined by examining the user agent string. The class supports asset
     * path retrieval for Windows and Android platforms.
     */
    
    static instance;
    constructor() {
        if (AssetPathManager.instance) {
            return AssetPathManager.instance;
        }
        this.path = String.raw;
        this.windowsGraphPath = this.path`F:\G\main`;

        this.config = {
            Windows: `assets:///${encodeURIComponent(this.windowsGraphPath)}/assets`,
            Android: 'http://localhost/_capacitor_file_/storage/emulated/0/L/logsec/main/assets'
        };

        AssetPathManager.instance = this;
    }

    getAssetPath(userAgent = navigator.userAgent) {
        /**
         * Retrieves the asset path based on the user's platform.
         * 
         * This method determines the user's operating system by examining the user agent string
         * and returns the corresponding asset path from the configuration. If the platform is not
         * recognized, it throws an error.
         * 
         * @param {string} userAgent - The user agent string of the browser, defaulting to navigator.userAgent.
         * @returns {string} The asset path for the detected platform.
         * @throws {Error} If the platform is unknown or the asset path is not configured.
         */

        const platformKey = Object.keys(this.config).find(os => userAgent.includes(os));
        if (!platformKey) {
            throw new Error('Unknown platform or asset path');
        }
        return this.config[platformKey];
    }
}

window.logseqAssetPath = function () {
    /**
     * Retrieves the base asset path for custom JavaScript imports across platforms.
     *
     * This function initializes the AssetPathManager to obtain the user's asset path,
     * enabling custom scripts to import modules by appending the necessary relative paths.
     * It handles platform-specific differences, returning null and logging errors if the
     * path retrieval fails.
     *
     * @returns {string|null} The asset path for the user's platform or undefined if an error occurs.
     */

    const manager = new AssetPathManager();
    let platformAssetPath = null;
    try {
        platformAssetPath = manager.getAssetPath();
    } catch (error) {
        console.error(error);
    }
    return platformAssetPath;
};


(function () {
    /**
     * Load and run logseq-tabler-icon-search
     */
    let logseqTablerIconSearch = document.createElement('script');
    logseqTablerIconSearch.type = 'module';
    logseqTablerIconSearch.src = logseqAssetPath() + '/logseq-tabler-icon-search/main.js';
    document.body.appendChild(logseqTablerIconSearch);
})();