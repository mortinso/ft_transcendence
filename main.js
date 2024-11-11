let pageState = 'overview'
let user = getUserData();
let loggedIn = true;

window.onpopstate = function (event) {
    if (event.state !== null) {
        pageState = event.state;
        changeContent(pageState, false);
    }
}

function login() {
    loggedIn = true;
    document.getElementById('header').style.display = 'block';
    history.replaceState(pageState, null, "");
    changeContent('overview', false);
}

function initialize() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.setAttribute('data-bs-theme', 'dark');
    }
    else {
        document.body.setAttribute('data-bs-theme', 'light');
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (e.matches) {
            document.body.setAttribute('data-bs-theme', 'dark');
        }
        else {
            document.body.setAttribute('data-bs-theme', 'light');
        }
    });

    if (!loggedIn) {
        changeContent('signin', false);
        document.getElementById('header').style.display = 'none';
    }
    else {

        history.replaceState(pageState, null, "");
        changeContent(pageState, false);
    }
}

function changeContent(page, pushState = true) {
    var contentDiv = document.getElementById('content');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/src/pages/${page}.html`, true);
    xhr.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200) {
            contentDiv.innerHTML = `<h2>Content not found!</h2>`
            return;
        }
        contentDiv.innerHTML = this.responseText;
        pageState = page;
        if (pushState && history.state !== pageState) {
            history.pushState(pageState, null, "");
        }
    }
    xhr.send();
}

// REST api call to get user data
function getUserData() {
    const url = 'http://localhost:8080/api/users/1';
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return data;
        });
}

function updateValues() {
    console.log(user.username, user);
    document.getElementById('username').innerText = `Hello ${user.username}`;
    document.getElementById('games-played').innerText = `Games played: ${user.games_played}`;
    document.getElementById('wins').innerText = `Wins: ${user.wins}`;
    document.getElementById('losses').innerText = `Losses: ${user.losses}`;
    document.getElementById('friends-online').innerText = `Friends online: ${user.friends_online}`;
}

initialize();