function initChatPage() {
    getUserData().then(user => {
        return user;
    }).then(user => {
        _user = user;
        fillFriendList();
    });
    translateAll();
}

async function fillFriendList() {
    const friendList = document.getElementById('friend-list');
    friendList.innerHTML = '';

    let friendListTemplate = document.getElementById('friend-list-template');
    if (_user.friends.length === 0 && _user.friend_requests.length === 0) {
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = i18next.t('livechat.noFriends');
        clone.querySelector('small').classList.add('d-none');
        clone.querySelector('img').classList.add('d-none');
        clone.querySelector('li').classList.add('disabled');
        clone.querySelector('button').classList.add('d-none');
        friendList.appendChild(clone);
    }

    if (_user.friend_requests.length > 0) {
        let friendRequestTemplate = document.getElementById('friend-request-template');
        for (let request of _user.friend_requests) {
            let clone = friendRequestTemplate.content.cloneNode(true);
            let user = (await getUserByID(request));
            clone.querySelector('h6').textContent = user.username;
            clone.querySelector('img').src = user.avatar;
            friendList.appendChild(clone);
        }
        friendList.appendChild(document.createElement('hr'));
    }

    for (let friendID of _user.friends) {
        let friend = await getUserByID(friendID);
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = friend.username;
        clone.querySelector('small').textContent = friend.is_online === true ? '🟢' : '⚫';
        clone.querySelector('img').src = friend.avatar;
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
    let input = document.getElementById('chat-input');
    input?.focus();
    input?.setAttribute('placeholder', i18next.t('livechat.chatPlaceholder'));
}

function showFriendOptions(event) {
    event.stopPropagation();
    translateAll();
}

function showAddFriendModal() {
    let addFriendModal = new bootstrap.Modal(document.getElementById('add-friend-modal'));
    addFriendModal.show();
    translateAll();
    let friendName = document.getElementById('inputFriendUsername');
    friendName.setAttribute('placeholder', i18next.t('common.username'));
}

async function addFriend() {
    let friendName = document.getElementById('inputFriendUsername');
    if (friendName.value === '') {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = i18next.t('livechat.emptyError');
        return;
    }
    if (friendName.value === _user.username) {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = i18next.t('livechat.selfError');
        return;
    }
    let friendList = document.getElementById('friend-list');
    for (let friend of friendList.children) {
        if (friend.querySelector('h6').innerText === friendName.value) {
            friendName.classList.add('is-invalid');
            document.getElementById('friend-name-error').innerText = i18next.t('livechat.alreadyFriendError');
            return;
        }
    }
    let result = await addFriendAsync(friendName.value).catch(error => {
        console.error(error);
    });
    if (result.status === 404) {
        friendName.classList.add('is-invalid');
        document.getElementById('friend-name-error').innerText = i18next.t('livechat.unkownUserError');
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
    const friendName = button.parentElement.parentElement.querySelector('h6').innerText;
    await acceptFriendRequestAsync(friendName);
    _user = await getUserData();
    fillFriendList();
}

function showRemoveFriendModal(button){
    const friendName = button.parentElement.parentElement.parentElement.querySelector('h6').innerText;
    let removeFriendModal = new bootstrap.Modal(document.getElementById('del-block-friend-modal'));
    removeFriendModal._element.querySelector('h1').innerText = i18next.t('livechat.removeFriend');
    removeFriendModal._element.querySelector('p').innerText =`${i18next.t('livechat.removeFriendQuestion1')} "${friendName}" ${i18next.t('livechat.removeFriendQuestion2')}`;
    removeFriendModal._element.querySelector('.btn-danger').addEventListener('click', () => removeFriend(button));
    removeFriendModal.show();
}

async function removeFriend(button){
    const friendName = button.parentElement.parentElement.parentElement.querySelector('h6').innerText;
    await removeFriendAsync(friendName);
    _user = await getUserData();
    fillFriendList();
}

async function rejectFriendRequest(button){
    const friendName = button.parentElement.parentElement.querySelector('h6').innerText;
    await rejectFriendRequestAsync(friendName);
    _user = await getUserData();
    fillFriendList();
}
