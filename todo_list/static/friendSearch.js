const userSearchBar = document.getElementById('userSearch');
const userSearchList = document.getElementById('userSearchList');

userSearchBar.addEventListener('input', (e) => {
    userSearchList.innerHTML = '';
    if (e.target.value === "") {
        userSearchList.insertAdjacentHTML('afterbegin', '<li>No se ha buscado nada todavía</li>');
    } else {
        fetch(`http://127.0.0.1:5000/friends/search-user/${e.target.value}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    userSearchList.insertAdjacentHTML('afterbegin', `<li>Nothing found.</li>`);
                } else {
                    data.forEach(user => {
                        userSearchList.insertAdjacentHTML('afterbegin', `<li>${user}</li>`);
                    });
                }
            });
    }
})