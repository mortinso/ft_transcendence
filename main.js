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
        changeContent('login', false);
        document.getElementById('header').style.display = 'none';
    }
    else {
        history.replaceState(pageState, null, "");
        changeContent(pageState, false);
    }
}

function checkLogin() {
    let jwt = sessionStorage.getItem('jwt');
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
    document.getElementById('loginLoading').classList.toggle('d-none');
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
            document.getElementById('loginLoading').classList.toggle('d-none');
        }
        else {
            alert('Login failed!');
            document.getElementById('loginLoading').classList.toggle('d-none');
            return;
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('loginFailModal'));
        modal.show();
        document.getElementById('loginLoading').classList.toggle('d-none');
        //log error
    });

    if (loggedIn) {
        document.getElementById('header').style.display = 'block';
        history.replaceState(pageState, null, "");
        changeContent('overview', false);
    }
}

async function logout() {
    const url = 'http://localhost:8080/api/auth/logout/';
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            refresh: sessionStorage.getItem('refresh')
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
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
            return;
        }
        else {
            alert('Logout failed!');
            return;
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('loginFailModal'));
        modal.show();
        document.getElementById('loginLoading').classList.toggle('d-none');
        //log error
    });

    sessionStorage.removeItem('jwt');
    sessionStorage.removeItem('refresh');
    loggedIn = false;
    document.getElementById('header').style.display = 'none';
    changeContent('login', false);
}

function signup(event) {
    event.preventDefault();
    let username = document.getElementById('signupUsername');
    let email = document.getElementById('signupEmail');
    let password = document.getElementById('signupPassword');
    let confirmPassword = document.getElementById('signupConfirmPassword');

    if (username.value === '' || email.value === '' || password.value === '' || confirmPassword.value === '')
        return;
    if (password.value !== confirmPassword.value) {
        document.getElementById('signupConfirmPassword').classList.add('is-invalid');
        return;
    }
    else
        document.getElementById('signupConfirmPassword').classList.remove('is-invalid');

    const url = 'http://localhost:8080/api/auth/signup/';
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value,
            confirm_password: confirmPassword.value
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    }).then(response => {
        if (response.status === 400) {
            document.getElementById('signupUsername').classList.add('is-invalid');
            console.warn(response);
            return;
        }
        else if (response.status === 201) {
            return response.json();
        }
        else {
            //log error
            return;
        }
    }).then(data => {
        if (data !== undefined) {
            const alertPlaceholder = document.getElementById('signupSuccessAlert');
            const appendAlert = (message, type) => {
                const wrapper = document.createElement('div')
                wrapper.innerHTML = [
                    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
                    `   <div>${message}</div>`,
                    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                    '</div>'
                ].join('')
        
                alertPlaceholder.append(wrapper)
            }
            appendAlert('Account created sucessfully! You may login now.', 'success');
            email.value = '';
            username.value = '';
            password.value = '';
            confirmPassword.value = '';
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('signupFailModal'));
        modal.show();
        //log error
    });
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
            case 'login':
                break;
            case 'signup':
                document.getElementById('signupForm').addEventListener('submit', signup, true);
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