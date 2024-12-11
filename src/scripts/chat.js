function initChatPage() {
    getUserData().then(user => {
        return user;
    }).then(user => {
        _user = user;
        fillFriendList();
    });
}

async function fillFriendList() {
    const friendList = document.getElementById('friend-list');
    friendList.innerHTML = '';

    let friendListTemplate = document.getElementById('friend-list-template');
    if (_user.friends.length === 0 && _user.friend_requests.length === 0) {
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = 'No friends yet';
        clone.querySelector('small').classList.add('d-none');
        clone.querySelector('img').classList.add('d-none');
        clone.querySelector('li').classList.add('disabled');
        friendList.appendChild(clone);
    }

    if (_user.friend_requests.length > 0) {
        let friendRequestTemplate = document.getElementById('friend-request-template');
        for (let request of _user.friend_requests) {
            let clone = friendRequestTemplate.content.cloneNode(true);
            let username = await getUsernameByID(request);
            clone.querySelector('h6').textContent = username;
            clone.querySelector('img').src = request.picture;
            friendList.appendChild(clone);
        }
        friendList.appendChild(document.createElement('hr'));
    }

    for (let friend of _user.friends) {
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = await getUsernameByID(friend);
        clone.querySelector('small').textContent = friend.status === 'online' ? '🟢' : '⚫';
        clone.querySelector('img').src = friend.picture;
        friendList.appendChild(clone);
    }
}

function toggleSelectedFriend(element) {
    const friendList = document.getElementById('friend-list');
    for (let friend of friendList.children) {
        friend.classList.remove('active');
    }
    element.classList.add('active');
    document.getElementById('selected-friend').innerText = element.querySelector('h6').innerText;
    let chatArea = document.getElementById('chat-area');
    if (chatArea.classList.contains('d-none')) {
        chatArea.classList.remove('d-none');
    }
}

function showFriendOptions(event) {
    event.stopPropagation();
}

function showAddFriendModal() {
    let addFriendModal = new bootstrap.Modal(document.getElementById('add-friend-modal'));
    addFriendModal.show();
}

async function addFriend() {
    let friendName = document.getElementById('inputFriendUsername');
    if (friendName.value === '') {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = 'Name cannot be empty';
        return;
    }
    if (friendName.value === _user.username) {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = 'You cannot add yourself as a friend';
        return;
    }
    let friendList = document.getElementById('friend-list');
    for (let friend of friendList.children) {
        if (friend.querySelector('h6').innerText === friendName.value) {
            friendName.classList.add('is-invalid');
            document.getElementById('friend-name-error').innerText = 'User is already your friend';
            return;
        }
    }
    let result = await addFriendAsync(friendName.value).catch(error => {
        console.error(error);
    });
    if (result.status === 404) {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = 'User not found';
        return;
    }
    else if (result.status === 200) {
        friendName.classList.remove('is-invalid');
        friendName.value = '';
        await fillFriendList();
        let addFriendModal = bootstrap.Modal.getInstance(document.getElementById('add-friend-modal'));
        addFriendModal.hide();
    }
}

async function acceptFriendRequest(button){
    let friendName = button.parentElement.parentElement.querySelector('h6').innerText;
    acceptFriendRequestAsync(friendName).then(() => {
        fillFriendList();
    });
}