const userSearchBar = document.getElementById('userSearch');
const userSearchList = document.getElementById('userSearchList');

function AddFriend(event, friendName) {
    var target = event.target;

    fetch(`./add?user=${friendName}`)
    .then(response => {
        if (response.status === 200) {
            target.parentNode.insertAdjacentHTML('beforeend', '<span>Enviado.</span>');
            target.remove();
        }
    });
}

function RequestAction(event, action, friendName) {
    var target = event.target;
    
    fetch(`./request?action=${action}&to_user=${friendName}`)
    .then(response => {
        if (response.status === 200) {
            parent = target.parentNode;
            parent.lastElementChild.remove();
            parent.lastElementChild.remove();
            console.log()
            relationStatus = action === 'accept' ? '<span class="accept">Aceptado.</span>' : '<span class="reject">Rechazado.</span>'
            parent.insertAdjacentHTML('beforeend', ` ${relationStatus}`);
        }
    });
}

userSearchBar.addEventListener('input', (e) => {
    let liElement = document.createElement('li');
    liElement.classList.add('no-search');
    liElement.textContent = 'Actualizando...'; 
    userSearchList.insertAdjacentElement('afterbegin', liElement);
    if (e.target.value === "") {
        userSearchList.innerHTML = '';
        liElement.textContent = 'No se ha buscado nada todavía.'; 
        userSearchList.insertAdjacentElement('afterbegin', liElement);
    } else {
        fetch(`./search-user?user=${e.target.value}`)
            .then(response => response.json())
            .then(data => {
                userSearchList.innerHTML = '';
                if (data.length === 0) {
                    liElement.textContent = 'No se encontró nada.'
                    userSearchList.insertAdjacentElement('afterbegin', liElement);
                } else {
                    data.forEach(user => {
                        var relationStatus = user[1] ? '<span>Enviado.</span>' : `<button onclick="AddFriend(event, '${user[0]}');">Agregar</a></li>`;
                        userSearchList.insertAdjacentHTML('afterbegin', 
                            `<li class="search-result"><img src="${user[2]}" alt="Foto de perfil de ${user[0]}"><a href="../${user[0]}">${user[0]}</a> ${relationStatus}`);
                    });
                }
            });
    }
})