
let _user = null;

function updateSettingsPage(){
    getUserData().then(user => {
        console.log(user.username, user);
        document.getElementById('userName').innerText = `${user.username}`;
        document.getElementById('userEmail').innerText = `${user.email}`;
        return user;
    }).then(user => {
        _user = user;
        loadAccountSettings(_user);
    });
}

function loadAccountSettings(){
    var contentDiv = document.getElementById('settings-container');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/src/pages/settings-account.html`, true);
    xhr.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200) {
            contentDiv.innerHTML = `<h2>Content not found!</h2>`
            return;
        }
        contentDiv.innerHTML = this.responseText;
        document.getElementById('InputUsername')?.setAttribute('placeholder', _user?.username);
        document.getElementById('InputEmail')?.setAttribute('placeholder', _user?.email);
        var form = document.getElementById('accountDetailsForm');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            updateAccountDetails(); 
        });
    }
    xhr.send();
}

function updateAccountDetails(){
    let newUser = getUpdatedAccountDetails();
    console.log(newUser);
    if (newUser === undefined)
        return;
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', `/api/users/1/edit`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200) {
            console.log('Error updating user details');
            return;
        }
        console.log('User details updated');
        updateSettingsPage();
    }
    xhr.send(JSON.stringify(newUser));
}

function getUpdatedAccountDetails(){
    let username = document.getElementById('InputUsername').value.trim();
    let email = document.getElementById('InputEmail').value.trim();

    let usernameInput = document.getElementById('InputUsername');
    if(username !== ''){
        if (username.match(/^[a-zA-Z0-9_\+\-\.\@]+$/)){
            usernameInput.classList.remove('is-invalid');
            usernameInput.classList.add('is-valid');
        }
        else{
            usernameInput.classList.remove('is-valid');
            usernameInput.classList.add('is-invalid');
            return;
        }
    }
    else{
        usernameInput.classList.remove('is-valid');
        usernameInput.classList.remove('is-invalid');
    }

    let emailInput = document.getElementById('InputEmail');
    if (email !== ''){
        if (email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)){
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid');
        }
        else{
            emailInput.classList.remove('is-valid');
            emailInput.classList.add('is-invalid');
            return;
        }
    }
    else{
        emailInput.classList.remove('is-valid');
        emailInput.classList.remove('is-invalid');
    }
    let newUser = {
        username: username !== '' ? username : _user.username,
        email: email !== '' ? email : _user.email
    }
    return newUser;
}

function loadSecuritySettings(){
    var contentDiv = document.getElementById('settings-container');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/src/pages/settings-security.html`, true);
    xhr.onreadystatechange = function () {
        if (this.readyState !== 4)
            return;
        if (this.status !== 200) {
            contentDiv.innerHTML = `<h2>Content not found!</h2>`
            return;
        }
        contentDiv.innerHTML = this.responseText;
        var form = document.getElementById('accountSecurityForm');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            updateSecurityDetails();
        });
    }
    xhr.send();
}

function updateSecurityDetails(){
    //TODO implement update security details
}

function deleteAccount(){
    //TODO replace with modal with confirmation
    alert('Are you sure you want to delete your account?\nThis action cannot be undone!');
}