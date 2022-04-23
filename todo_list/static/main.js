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
    if (input.value !== "") {
        document.querySelector(`label[for=${input.getAttribute('name')}]`).classList.add('focus');
        document.querySelector(`label[for=${input.getAttribute('name')}]`).classList.add('current-focus');
    }
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

// NAV de página de inicio

if (topbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 0) {
            topbar.classList.remove('in-start');
        } else {
            topbar.classList.add('in-start');
        }
    })
}

// Smooth scroll from anchor
function scrollToInfo() {
    document.querySelector("#info").scrollIntoView({
        behavior: 'smooth'
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});