//Login user
async function login(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const keepLoggedIn = document.getElementById('keepLogin').checked;
    if (keepLoggedIn)
        localStorage.setItem('keepLoggedIn', true);
    else
        localStorage.removeItem('keepLoggedIn');
    const url = '/api/auth/login/';
    document.getElementById('loginLoading').classList.toggle('d-none');
    await fetch(url, {
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
            document.getElementById('loginUsername').classList.remove('is-invalid');
            document.getElementById('loginPassword').classList.remove('is-invalid');
            return response.json();
        }
        else if (response.status === 502) {
            throw new Error('Server error');
        }
        else {
            document.getElementById('loginUsername').classList.add('is-invalid');
            document.getElementById('loginPassword').classList.add('is-invalid');
            return null;
        }
    }).then(data => {
        if (data == null){
            document.getElementById('loginLoading').classList.toggle('d-none');
            return;
        }
        if (data.detail === 'Email sent.')
        {
            let modal = new bootstrap.Modal(document.getElementById('f2aModal'));
            modal.show();
            return;
        }
        if (data !== null) {
            sessionStorage.setItem('jwt', data.access);
            sessionStorage.setItem('refresh', data.refresh);
            if (keepLoggedIn)
                localStorage.setItem('refresh', data.refresh);
            loggedIn = true;
            document.getElementById('loginLoading').classList.toggle('d-none');
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('loginFailModal'));
        modal.show();
        document.getElementById('loginLoading').classList.toggle('d-none');
        translateAll();
        //TODO: log error
    });

    postLogin();
}

// Adicione esta função para processar o retorno do OAuth
function handleOAuthReturn() {
    const urlParams = new URLSearchParams(window.location.search);
    const access = urlParams.get('access');
    const refresh = urlParams.get('refresh');
    
    if (access && refresh) {
        // Salvar tokens no sessionStorage
        sessionStorage.setItem('jwt', access);
        sessionStorage.setItem('refresh', refresh);
        
        // Se o usuário selecionou "manter conectado"
        if (localStorage.getItem('keepLoggedIn') === 'true') {
            localStorage.setItem('refresh', refresh);
        }
        
        // Atualizar estado
        loggedIn = true;
        
        // Limpar a URL para não manter os tokens expostos
        history.replaceState({}, document.title, window.location.pathname);
        
        // Inicializar a página
        postLogin();
    }
}

async function loginWith42(){
    window.location.href = '/api/oauth/login';
}

// Adicione este código ao evento de carregamento da página
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se há tokens na URL (retorno de OAuth)
    handleOAuthReturn();
    
    // Verificar se há um token de refresh armazenado (login anterior)
    if (!loggedIn && (localStorage.getItem('refresh') || sessionStorage.getItem('refresh'))) {
        const storedRefresh = localStorage.getItem('refresh') || sessionStorage.getItem('refresh');
        sessionStorage.setItem('refresh', storedRefresh);
        
        // Tenta renovar o token usando o refresh token
        refreshLogin().then(() => {
            if (sessionStorage.getItem('jwt')) {
                loggedIn = true;
                postLogin();
            }
        });
    }
});

//Initialize main page after login
async function postLogin(){
    if (loggedIn) {
        document.getElementById('header').style.display = 'block';
        _user = await getUserData();
        await getNotifications();
        await getUserAvatar(_user.id).then(avatar => { _avatar = avatar; });
        document.getElementById('header-avatar').src = _avatar;
        changeContent('overview', true);
        history.replaceState(pageState, null, "");
    }
}

//Confirm the 2FA code
async function confirmF2A() {
    const keepLoggedIn = document.getElementById('keepLogin').checked;
    if (keepLoggedIn)
        localStorage.setItem('keepLoggedIn', true);
    else
        localStorage.removeItem('keepLoggedIn');
    let input = document.getElementById('login2FA');
    let f2a = input?.value;
    if (f2a === '' || f2a == undefined) {
        input.classList.add('is-invalid');
        return;
    }
    input.classList.remove('is-invalid');
    const url = '/api/auth/check_otp/';
    await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            otp: f2a,
            purpose: 'tfa'
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    }).then(response => {
        if (response.status === 200) {
            let r = response.json();
            return r;
        }
        else {
            return null;
        }
    }).then(data => {
        if (data !== null) {
            let modelElm = document.getElementById('f2aModal');
            let modal = bootstrap.Modal.getInstance(modelElm);
            input.classList.remove('is-invalid');
            input.value = '';
            modal.hide();

            sessionStorage.setItem('jwt', data.access);
            sessionStorage.setItem('refresh', data.refresh);
            if (keepLoggedIn)
                localStorage.setItem('refresh', data.refresh);
            loggedIn = true;
            document.getElementById('loginLoading').classList.toggle('d-none');

            postLogin();
        }
        else {
            let input = document.getElementById('login2FA');
            input.classList.add('is-invalid');
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('loginFailModal'));
        modal.show();
        //log error
        console.error(error);
    });
}

//Logout the user
async function logout() {
    const url = '/api/auth/logout/';
    await fetch(url, {
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
    clearSession();
}

//Clear the session
function clearSession() {
    sessionStorage.removeItem('jwt');
    sessionStorage.removeItem('refresh');
    localStorage.removeItem('refresh');
    loggedIn = false;
    _user = null;
    document.getElementById('header').style.display = 'none';
    document.getElementById('notification-area').innerHTML = '';
    changeContent('login', false);
}

//Create a new user account
function signup(event) {
    event.preventDefault();
    let username = document.getElementById('signupUsername');
    let email = document.getElementById('signupEmail');
    let password = document.getElementById('signupPassword');
    let confirmPassword = document.getElementById('signupConfirmPassword');

    document.getElementById('signupUsername').classList.remove('is-invalid');
    if (username.value === '' || email.value === '' || password.value === '' || confirmPassword.value === '')
        return;
    if (password.value !== confirmPassword.value) {
        document.getElementById('signupConfirmPassword').classList.add('is-invalid');
        return;
    }
    else
        document.getElementById('signupConfirmPassword').classList.remove('is-invalid');
    const url = '/api/auth/signup/';
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
            //TODO: check if username or email is already taken
            document.getElementById('signupUsername').classList.add('is-invalid');
            console.warn(response);
            return;
        }
        else if (response.status === 201 || response.status === 200) {
            return response.json();
        }
        else {
            throw new Error('Error creating account');
        }
    }).then(data => {
        if (data !== undefined) {
            showOTPModal();
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('signupFailModal'));
        modal.show();
        translateAll();
        //log error
        console.error(error);
    });
}

function showOTPModal() {
    let modal = new bootstrap.Modal(document.getElementById('signupSuccessModal'));
    modal.show();
    document.getElementById('signupOTP').focus();
}

//Confirm the OTP
async function confirmSignup() {
    let input = document.getElementById('signupOTP');
    let otp = input?.value;
    if (otp === '' || otp == undefined) {
        input.classList.add('is-invalid');
        return;
    }
    input.classList.remove('is-invalid');
    const url = '/api/auth/check_otp/';
    await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            otp: otp,
            purpose: 'signup'
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    }).then(response => {
        if (response.status === 201) {
            let r = response.json();
            return r;
        }
        else {
            return null;
        }
    }).then(data => {
        if (data !== null) {
            let modelElm = document.getElementById('signupSuccessModal');
            let modal = bootstrap.Modal.getInstance(modelElm);
            input.classList.remove('is-invalid');
            input.value = '';
            modal.hide();
            const appendAlert = (message, type) => {
                const wrapper = document.createElement('div')
                wrapper.innerHTML = [
                    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
                    `   <div>${message}</div>`,
                    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                    '</div>'
                ].join('')
                const alertPlaceholder = document.getElementById('signupSuccessAlert');
                alertPlaceholder.append(wrapper)
            }
            appendAlert(i18next.t('login.accountCreated'), 'success');
        }
        else {
            let input = document.getElementById('signupOTP');
            input.classList.add('is-invalid');
        }
    }).catch(error => {
        let modal = new bootstrap.Modal(document.getElementById('signupFailModal'));
        modal.show();
        //log error
        console.error(error);
    });
}

//Get user data
//TODO change to be able to get any user instead of just the logged in user
async function getUserData() {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            "Content-Type": "application/json",
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        let data = await refreshLogin();
        return data;
    }
    if (response.status !== 200) {
        console.error('Error fetching user data');
        logout();
        return;
    };
    const data = await response.json();
    return data;
}

//Get the user ID from the access token
async function getUserID() {
    try {
        if (sessionStorage.getItem('jwt') === null)
            await refreshLogin();
        const payload = sessionStorage.getItem('jwt').split('.')[1];
        return JSON.parse(atob(payload))?.user_id;
    }
    catch (e) {
        return null;
    }
}

//Refresh the login token
async function refreshLogin() {
    if (sessionStorage.getItem('refresh') !== null) {
        const refreshToken = sessionStorage.getItem('refresh');
        const url = '/api/auth/token/refresh/';
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                refresh: refreshToken
            }),
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
            }
        }).then(response => {
            if (response.status === 200) {
                return response.json();
            }
            else {
                console.error('Error refreshing token', response);
                return null;
            }
        }).then(data => {
            if (data !== null) {
                sessionStorage.setItem('jwt', data.access);
                sessionStorage.setItem('refresh', data.refresh);
                if (localStorage.getItem('keepLoggedIn') === true)
                    localStorage.setItem('refresh', data.refresh);
                return getUserData();
            }
            else {
                clearSession();
                return;
            }
        });
        return response;
    }
    return null;
}

//Verify the refresh token
async function verifyRefreshToken(refresh) {
    const url = '/api/auth/token/refresh/';
    await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            refresh: refresh
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
        }
    }).then(response => {
        return response.status === 200;
    }).catch(error => {
        return false;
    });
}

//Add a friend
async function addFriendAsync(friendName) {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/invite_friend/`;
    const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify({
            add_friend: friendName
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await addFriendAsync(friendName);
    }
    return response;
}

//Get a user by ID
async function getUserByID(userID) {
    const url = `/api/users/${userID}/`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await getUserByID(userID);
    }
    const data = await response.json();
    return data;
}

//Accept a friend request
async function acceptFriendRequestAsync(friendID) {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/accept_friend/`;
    const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify({
            accept_friend: friendID
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await acceptFriendRequestAsync(friendID);
    }
    return response;
}

//Remove a friend
async function removeFriendAsync(friendName) {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/remove_friend/`;
    const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify({
            remove_friend: friendName
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await removeFriendAsync(friendName);
    }
    return response;
}

//Reject a friend request
async function rejectFriendRequestAsync(friendName) {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/remove_friend_request/`;
    const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify({
            remove_friend: friendName
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await rejectFriendRequestAsync(friendName);
    }
    return response;
}

//Block a user
async function blockUserAsync(userName) {
    const userID = await getUserID();
    if (userID === null)
        return;
    const url = `/api/users/${userID}/block/`;
    const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify({
            user: userName
        }),
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status === 401) {
        await refreshLogin();
        return await blockUserAsync(userName);
    }
    return response;
}

//Get the user avatar
async function getUserAvatar(userID) {
    let url = `/api/users/${userID}/get_avatar/`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
            }
        });
        if (response.ok) {
            const blob = await response.blob();
            const objectURL = URL.createObjectURL(blob);
            return objectURL;
        } else {
            console.error('Error fetching avatar');
            return null;
        }
    } catch (error) {
        console.error('Error fetching avatar', error);
        return null;
    }
}