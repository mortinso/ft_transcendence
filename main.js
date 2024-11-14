let pageState = 'overview'
let loggedIn = true;

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

    if (!loggedIn) {
        changeContent('signin', false);
        document.getElementById('header').style.display = 'none';
    }
    else {

        history.replaceState(pageState, null, "");
        changeContent(pageState, false);
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
            alert('Login successful!');
            console.log(data);
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
    }
    xhr.send();
}

initialize();