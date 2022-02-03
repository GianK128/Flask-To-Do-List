const sidebar = document.querySelector('.sidebar');
const topbar = document.querySelector('.topbar');
const menuBtn = document.getElementById('menuBtn');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const darkModeToggle = document.querySelector('.dark-light-toggle');
const closable = document.querySelectorAll('.close');

closable.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.remove()
    })
})

if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        sidebar.toggleAttribute('open');
    })
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        topbar.toggleAttribute('open');
    })
}

darkModeToggle.addEventListener('click', () => {
    document.body.toggleAttribute('dark-mode');
    let theme = document.body.hasAttribute('dark-mode');

    if (theme) {
        localStorage.setItem('preferred-theme', 'dark');
        if (darkModeText) {
            darkModeText.textContent = 'Modo claro';
        }
    } else {
        localStorage.setItem('preferred-theme', 'light');
        if (darkModeText) {
            darkModeText.textContent = 'Modo oscuro';
        }
    }
})