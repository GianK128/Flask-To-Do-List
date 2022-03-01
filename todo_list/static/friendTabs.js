document.querySelectorAll('button.tab').forEach(btn => {
    btn.addEventListener('click', e => {
        e.target.closest('.tab-switcher').setAttribute('open-tab', btn.getAttribute('for-tab'));
    });
});