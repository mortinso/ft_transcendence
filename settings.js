
function updateSettingsPage(){
    getUserData().then(user => {
        console.log(user.username, user);
        document.getElementById('userName').innerText = `${user.username}`;
        document.getElementById('userEmail').innerText = `${user.email}`;
        return user;
    }).then(user => {
        loadAccountSettings(user);
    });
}

function loadAccountSettings(user){
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
        document.getElementById('InputUsername')?.setAttribute('placeholder', user?.username);
        document.getElementById('InputEmail')?.setAttribute('placeholder', user?.email);
        var form = document.getElementById('accountDetailsForm');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            updateAccountDetails(user); 
        });
    }
    xhr.send();
}

function updateAccountDetails(user){
    let username = document.getElementById('InputUsername').value.trim();
    let email = document.getElementById('InputEmail').value.trim();

    let usernameInput = document.getElementById('InputUsername');
    if(username !== ''){
        if (username.match(/^[a-zA-Z0-9_]+$/)){
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
    var user = {
        username: username !== '' ? username : user.username,
        email: email !== '' ? email : user.email
    }
    console.log(user);
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
        var form = document.getElementById('accountDetailsForm');
        form.addEventListener('submit', function(e){
            e.preventDefault();
            updateSecurityDetails(user);
        });
    }
    xhr.send();
}

function updateSecurityDetails(user){
    //TODO implement update security details
}

function deleteAccount(){
    //TODO replace with modal with confirmation
    alert('Are you sure you want to delete your account?\nThis action cannot be undone!');
}