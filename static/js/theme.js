/* ============================================
   DARK MODE THEME TOGGLE
   ============================================ */

const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

// Initialize theme
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = prefersDark.matches ? 'dark' : 'light';
    const theme = savedTheme || systemTheme;
    
    setTheme(theme);
}

// Set theme
function setTheme(theme) {
    const isDark = theme === 'dark';
    
    if (isDark) {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }
    
    updateThemeIcon(isDark);
}

// Update theme icon
function updateThemeIcon(isDark) {
    if (themeToggle) {
        themeToggle.innerHTML = isDark 
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zm0 2c4.418 0 8-3.582 8-8s-3.582-8-8-8-8 3.582-8 8 3.582 8 8 8zm8-8h3v2h-3zm-20 0h3v2H0zm17.657-5.657l2.121-2.121 1.414 1.414-2.121 2.121zm-12.728 12.728l2.121-2.121 1.414 1.414-2.121 2.121zm5.657-17.657l1.414-1.414 2.121 2.121-1.414 1.414zm-5.657 17.657l1.414-1.414 2.121 2.121-1.414 1.414z"/></svg>'
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
    }
}

// Toggle theme
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });
}

// Listen for system theme changes
prefersDark.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
    }
});

// Initialize on load
initTheme();
