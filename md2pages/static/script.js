// Restore scroll position on page load
window.addEventListener('load', () => {
  try {
    const key = location.pathname;
    const pos = localStorage.getItem(key);
    if (pos) {
      window.scrollTo(0, parseInt(pos, 10));
    }
  } catch (e) {
    // localStorage might not be available, ignore error
  }
});

// Save scroll position
const saveScrollPosition = () => {
  try {
    localStorage.setItem(location.pathname, String(window.scrollY));
  } catch (e) {
    // localStorage might not be available, ignore error
  }
};

// Save on page unload
window.addEventListener('beforeunload', saveScrollPosition);

// Save when page becomes hidden
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') {
    saveScrollPosition();
  }
});
