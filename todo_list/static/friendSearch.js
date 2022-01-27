const userSearchBar = document.getElementById('userSearch');
const userSearchList = document.getElementById('userSearchList');

function AddFriend(event, friendName) {
    var target = event.target;

    fetch(`http://127.0.0.1:5000/friends/add?user=${friendName}`)
    .then(response => {
        if (response.status === 200) {
            target.parentNode.insertAdjacentHTML('beforeend', '¡Solicitud enviada!');
            target.remove();
        }
    });
}

function RequestAction(event, action, friendName) {
    var target = event.target;
    
    fetch(`http://127.0.0.1:5000/friends/request?action=${action}&to_user=${friendName}`)
    .then(response => {
        if (response.status === 200) {
            parent = target.parentNode;
            parent.lastElementChild.remove();
            parent.lastElementChild.remove();
            console.log()
            relationStatus = action === 'accept' ? '¡Solicitud aceptada!' : 'Solicitud rechazada.'
            parent.insertAdjacentHTML('beforeend', ` ${relationStatus}`);
        }
    });
}

userSearchBar.addEventListener('input', (e) => {
    userSearchList.innerHTML = 'Actualizando...';
    if (e.target.value === "") {
        userSearchList.innerHTML = '';
        userSearchList.insertAdjacentHTML('afterbegin', '<li>No se ha buscado nada todavía</li>');
    } else {
        fetch(`http://127.0.0.1:5000/friends/search-user?user=${e.target.value}`)
            .then(response => response.json())
            .then(data => {
                userSearchList.innerHTML = '';
                if (data.length === 0) {
                    userSearchList.insertAdjacentHTML('afterbegin', `<li>Nothing found.</li>`);
                } else {
                    data.forEach(user => {
                        var relationStatus = user[1] ? '¡Solicitud enviada!' : `<button onclick="AddFriend(event, '${user[0]}');">Agregar</a></li>`;
                        userSearchList.insertAdjacentHTML('afterbegin', 
                            `<li><a href="http://127.0.0.1:5000/${user[0]}">${user[0]}</a> ${relationStatus}`);
                    });
                }
            });
    }
})