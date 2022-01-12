const userSearchBar = document.getElementById('userSearch');
const userSearchList = document.getElementById('userSearchList');

userSearchBar.addEventListener('input', (e) => {
    userSearchList.innerHTML = 'Actualizando...';
    if (e.target.value === "") {
        userSearchList.innerHTML = '';
        userSearchList.insertAdjacentHTML('afterbegin', '<li>No se ha buscado nada todavía</li>');
    } else {
        fetch(`http://127.0.0.1:5000/friends/search-user/${e.target.value}`)
            .then(response => response.json())
            .then(data => {
                userSearchList.innerHTML = '';
                if (data.length === 0) {
                    userSearchList.insertAdjacentHTML('afterbegin', `<li>Nothing found.</li>`);
                } else {
                    data.forEach(user => {
                        userSearchList.insertAdjacentHTML('afterbegin', 
                            `<li><a href="http://127.0.0.1:5000/lists/${user}">${user}</a> <a href="http://127.0.0.1:5000/friends/add/${user}">Agregar</a></li>`);
                    });
                }
            });
    }
})