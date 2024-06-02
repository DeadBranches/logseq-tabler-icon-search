(function () {
    const platformAssetPath = logseqAssetPath();
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        @font-face {
        font-family: "better-tabler-icons";
        font-style: normal;
        font-weight: 400;
        src: url("${platformAssetPath}/tabler-icon-fonts/tabler-icons.woff2") format("woff2"),
                url("${platformAssetPath}/tabler-icon-fonts/tabler-icons.woff") format("woff"),
                url("${platformAssetPath}/tabler-icon-fonts/tabler-icons.ttf") format("truetype"); // Corrected the file extension
        }
    `;
    document.head.appendChild(styleElement);

})();