function loadGoogleFonts() {
  const linkElement = document.createElement('link');
  linkElement.href = 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap';
  linkElement.rel = 'stylesheet';
  document.head.appendChild(linkElement);
}

export { loadGoogleFonts };