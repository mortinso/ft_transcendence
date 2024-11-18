let pageState = 'overview'
let loggedIn = false;

//Handle back and forward navigation events
window.onpopstate = function (event) {
    if (event.state !== null) {
        pageState = event.state;
        changeContent(pageState, false);
    }
}

//Initliaze the page
function initialize() {
    applyColorScheme();
    
    loggedIn = checkLogin();
    if (!loggedIn) {
        changeContent('signin', false);
        document.getElementById('header').style.display = 'none';
    }
    else {
        history.replaceState(pageState, null, "");
        changeContent(pageState, false);
    }
}

function checkLogin() {
    let jwt = sessionStorage.getItem('jwt');
    console.log(jwt);
    if (jwt !== null) {
        return true;
    }
    else {
        return false;
    }
}

async function login() {
    let username = document.getElementById('loginUsername').value;
    let password = document.getElementById('loginPassword').value;

    const url = 'http://localhost:8080/api/auth/login/';
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            password: password
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    }).then(response => {
        if (response.status === 200) {
            return response.json();
        }
        else {
            return null;
        }
    }).then(data => {
        if (data !== null) {
            sessionStorage.setItem('jwt', data.access);
            sessionStorage.setItem('refresh', data.refresh);
            loggedIn = true;
        }
        else {
            alert('Login failed!');
            return;
        }
    });

    if (loggedIn) {
        document.getElementById('header').style.display = 'block';
        history.replaceState(pageState, null, "");
        changeContent('overview', false);
    }
}

function logout() {
    sessionStorage.removeItem('jwt');
    sessionStorage.removeItem('refresh');
    loggedIn = false;
    document.getElementById('header').style.display = 'none';
    changeContent('signin', false);
}

//Set the color scheme based on the user's browser settings
function applyColorScheme() {
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
}

//Change the content of the page
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
        switch (page) {
            case 'overview':
                updateOverviewPage();
                break;
            case 'profile':
                updateProfilePage();
                break;
            case 'settings':
                updateSettingsPage();
                break;
            case 'signin':
                break;
            default:
                break;
        }
        updateHeaderButton(page);
    }
    xhr.send();
}

//Update header buttons based on the current page
function updateHeaderButton(page) {
    let overviewButton = document.getElementById('header-overview');
    let pongButton = document.getElementById('header-pong');
    let game2Button = document.getElementById('header-game2');
    let livechatButton = document.getElementById('header-livechat');

    let buttons = {
        'overview': overviewButton,
        'pong': pongButton,
        'game2': game2Button,
        'livechat': livechatButton
    };

    for (let key in buttons) {
        if (key === page) {
            buttons[key].classList.remove('link-body-emphasis');
        } else {
            buttons[key].classList.add('link-body-emphasis');
        }
    }
}

initialize();