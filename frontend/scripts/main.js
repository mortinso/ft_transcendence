let pageState = 'overview'
let loggedIn = false;
let _user = null;
let _avatar = null;
let _lang = 'EN';
var _running = false;

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
    if (localStorage.getItem('lang') !== null) {
        _lang = localStorage.getItem('lang');
    }
    await initTranslations();

    loggedIn = await checkLogin();
    window.localStorage.setItem('loggedIn', loggedIn);
    if (!loggedIn) {
        changeContent('login', false);
        document.getElementById('header').style.display = 'none';
        await new Promise(resolve => setTimeout(resolve, 100));
        if (window.sessionStorage.getItem('42error') !== null) {
            const error = window.sessionStorage.getItem('42error');
            switch (error) {
                case 'User already logged in.':
                    alert(i18next.t('login.alreadyLoggedIn'));
                    break;
                case 'User is deactivated.':
                    alert(i18next.t('login.deactivated'));
                    break;
                case !undefined:
                    alert(i18next.t('login.42error'));
                    break;
                default:
                    break;
            }
            window.sessionStorage.removeItem('42error');
        }
    }
    else {
        history.replaceState(pageState, null, "");
        _user = await getUserData();
        _lang = _user.idiom;
        await getNotifications();
        await getUserAvatar(_user.id).then(avatar => { _avatar = avatar; });
        changeContent(pageState, false);
        document.getElementById('header-avatar').src = _avatar;
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
    if (localStorage.getItem('theme') !== null) {
        document.body.setAttribute('data-bs-theme', localStorage.getItem('theme'));
    }
    else {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.setAttribute('data-bs-theme', 'dark');
        }
        else {
            document.body.setAttribute('data-bs-theme', 'light');
        }
    }
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (localStorage.getItem('theme') === null) {
            if (e.matches) {
                document.body.setAttribute('data-bs-theme', 'dark');
            }
            else {
                document.body.setAttribute('data-bs-theme', 'light');
            }
        }
    });
}

//Initialize the translation system
async function initTranslations() {
    await i18next.use(i18nextHttpBackend).init({
        lng: _lang,
        fallbackLng: 'EN',
        debug: true,
        backend: {
            loadPath: '/frontend/locales/{{lng}}/{{ns}}.json'
        }
    });
    translateAll();
}

//Translate all elements with the data-i18n attribute
function translateAll() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        let key = element.getAttribute('data-i18n');
        element.innerText = i18next.t(key);
    });
}

//Change the content of the page
function changeContent(page, pushState = true, params=null) {
    var contentDiv = document.getElementById('content');
    // Remove previously added scripts
    var oldScripts = document.querySelectorAll('script[data-dynamic]');
    oldScripts.forEach(script => script.remove());
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/frontend/pages/${page}.html`, true);
    xhr.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200) {
            contentDiv.innerHTML = `<h2>${i18next.t('common.contentNotFound')}</h2>`
            return;
        }
        contentDiv.innerHTML = this.responseText;
        // Execute scripts in the loaded content
        var scripts = contentDiv.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i++) {
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.setAttribute('data-dynamic', 'true'); // Mark script as dynamically added
            if (scripts[i].src) {
                script.src = scripts[i].src;
            } else {
                script.textContent = scripts[i].textContent;
            }
            document.head.appendChild(script);
        }
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
                updateProfilePage(params);
                break;
            case 'livechat':
                initChatPage();
                break;
            case 'settings':
                updateSettingsPage();
                break;
            case 'login':
                document.getElementById('loginForm').addEventListener('submit', login, true);
                translateAll();
                break;
            case 'signup':
                document.getElementById('signupForm').addEventListener('submit', signup, true);
                translateAll();
            default:
                break;
        }
        updateHeaderButton(page);
        if (_running !== undefined)
        {
            if (_running && page !== 'pong')
                _running = false;
        }
    }
    xhr.send();
}
//Update header buttons based on the current page
function updateHeaderButton(page) {
    let overviewButton = document.getElementById('header-overview');
    let pongButton = document.getElementById('header-pong');
    let game2Button = document.getElementById('header-game2');
    let friendsButton = document.getElementById('header-friends');
    let buttons = {
        'overview': overviewButton,
        'pong': pongButton,
        'game2': game2Button,
        'friends': friendsButton
    };
    for (let key in buttons) {
        if (key === page) {
            buttons[key].classList.remove('link-body-emphasis');
        } else {
            buttons[key].classList.add('link-body-emphasis');
        }
    }
}

//Get user notifications
async function getNotifications() {
    if (_user === null) {
        _user = await getUserData();
    }
    let notificationTemplate = document.getElementById('notification-template');
    let notificationContainer = document.getElementById('notification-area');
    for (let request of _user.friend_requests) {
        let notification = notificationTemplate.content.cloneNode(true);
        notification.querySelector('h6').innerText = i18next.t('notifications.friendRequest');
        let user = await getUserByID(request);
        notification.querySelector('p').innerText = `${user.username} ${i18next.t('notifications.friendRequestMessage')}`;
        notification.querySelector('a').addEventListener('click', () => { changeContent('livechat', true) });
        notificationContainer.appendChild(notification);
    }
    if (notificationContainer.children.length === 0) {
        notificationContainer.innerHTML = `<p class="d-flex mx-3 gap-3">${i18next.t('notifications.empty')}</p>`;
        document.getElementById('notification-icon').setAttribute('href', '#notification-empty');
    }
    if (notificationContainer.children.length > 0 && notificationContainer.getElementsByTagName('a').length > 0) {
        document.getElementById('notification-icon').setAttribute('href', '#notification-full');
    }
}
initialize();