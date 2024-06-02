class AssetPathManager {
    constructor() {
        this.config = {
            Windows: 'assets:///F%3A/G/main/assets',
            Android: 'http://localhost/_capacitor_file_/storage/emulated/0/L/logsec/main/assets'
        };
    }

    getAssetPath(userAgent = navigator.userAgent) {
        console.log("AssetPathManager.getAssetPath executed");

        const platformKey = Object.keys(this.config).find(os => userAgent.includes(os));
        if (!platformKey) {
            throw new Error('Unknown platform or asset path');
        }
        return this.config[platformKey];
    }
}

window.logseqAssetPath = function () {
    const manager = new AssetPathManager();
    let platformAssetPath;
    try {
        platformAssetPath = manager.getAssetPath();
    } catch (error) {
        console.error(error);
    }
    return platformAssetPath;
};

fetch(logseqAssetPath() + '/logseq-tabler-icon-search/index.html')
.then(response => response.text())
.then(htmlString => {
    document.body.insertAdjacentHTML('beforeend', htmlString);
    resolve();
})
.catch(error => {
    console.error('Error loading HTML:', error);
    reject(error);
});