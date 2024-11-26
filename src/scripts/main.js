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
async function initialize() {
    applyColorScheme();

    loggedIn = await checkLogin();
    if (!loggedIn) {
        changeContent('login', false);
        document.getElementById('header').style.display = 'none';
    }
    else {
        history.replaceState(pageState, null, "");
        changeContent(pageState, false);
    }
}

//Check if the user is logged in
async function checkLogin() {
    const jwt = sessionStorage.getItem('jwt');
    const refresh = localStorage.getItem('refresh');

    if (refresh !== null) {
        await verifyRefreshToken(refresh).then(valid => {
            if (!valid) {
                localStorage.removeItem('refresh');
                localStorage.removeItem('keepLoggedIn');
                return false;
            }
        });
    }
    if (jwt !== null || refresh !== null) {
        if (sessionStorage.getItem('refresh') === null) {
            sessionStorage.setItem('refresh', refresh);
        }
        return true;
    }
    else {
        return false;
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
        if (page !== 'login' && page !== 'signup')
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
            case 'livechat':
                initChatPage();
                break;
            case 'settings':
                updateSettingsPage();
                break;
            case 'login':
                document.getElementById('loginForm').addEventListener('submit', login, true);
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