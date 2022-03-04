const sidebar = document.querySelector('.sidebar');
const topbar = document.querySelector('.topbar');
const menuBtn = document.getElementById('menuBtn');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const darkModeToggle = document.querySelector('.dark-light-toggle');
const closable = document.querySelectorAll('.close');

// ALERTAS

closable.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.remove()
    })
})

// BOTONES DE MENU NAV

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

// BOTON DE MODO OSCURO

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

// MODALES

document.querySelectorAll('[open-modal]').forEach(modalBtn => {
    modalBtn.addEventListener('click', e => {
        document.getElementById(e.target.getAttribute('open-modal')).setAttribute('open', true);
    });
});

document.querySelectorAll('.close-modal').forEach(modalClose => {
    modalClose.addEventListener('click', e => {
        e.target.closest('.modal[open]').removeAttribute('open');
    });
});

// INPUTS BONITOS

document.querySelectorAll('form .inputs input').forEach(input => {
    input.addEventListener('focus', e => {
        let name = e.target.getAttribute('name');
        document.querySelector(`label[for=${name}]`).classList.add('focus');
        document.querySelector(`label[for=${name}]`).classList.add('current-focus');
    });
    input.addEventListener('focusout', e => {
        let name = e.target.getAttribute('name');
        if (e.target.value === "") {
            document.querySelector(`label[for=${name}]`).classList.remove('focus');
        }
        document.querySelector(`label[for=${name}]`).classList.remove('current-focus');
    });
});