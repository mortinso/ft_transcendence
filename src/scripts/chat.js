function initChatPage() {
    getUserData().then(user => {
        return user;
    }).then(user => {
        _user = user;
        fillFriendList();
    });
}

function fillFriendList() {
    const friendList = document.getElementById('friend-list');
    friendList.innerHTML = '';
    //test data
    // const friends = [
    //     {
    //         name:'Alice',
    //         status: 'online',
    //         picture: 'https://avatars.githubusercontent.com/u/107864891?v=4'
    //     }, 
    //     {
    //         name:'Bob',
    //         status: 'offline',
    //         picture: 'https://avatars.githubusercontent.com/u/107864891?v=4'
    //     },
    //     {
    //         name:'Charlie',
    //         status: 'online',
    //         picture: 'https://avatars.githubusercontent.com/u/107864891?v=4'
    //     },
    //     {
    //         name:'David',
    //         status: 'offline',
    //         picture: 'https://avatars.githubusercontent.com/u/107864891?v=4'
    //     }
    // ];

    //create a list item for each friend from template
    let friendListTemplate = document.getElementById('friend-list-template');
    if (_user.friends.length === 0) {
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = 'No friends yet';
        clone.querySelector('small').classList.add('d-none');
        clone.querySelector('img').classList.add('d-none');
        clone.querySelector('li').classList.add('disabled');
        friendList.appendChild(clone);
        return;
    }
    for (let friend of _user.friends) {
        let clone = friendListTemplate.content.cloneNode(true);
        clone.querySelector('h6').textContent = friend.name;
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

function showAddFriendModal() {
    let addFriendModal = new bootstrap.Modal(document.getElementById('add-friend-modal'));
    addFriendModal.show();
}

async function addFriend(){
    let friendName = document.getElementById('inputFriendUsername');
    if(friendName.value === ''){
        friendName.classList.add('is-invalid');
        return;
    }
    let friend = _user.friends.find(f => f.name === friendName.value);
    if(friend){
        alert('This user is already your friend');
        return;
    }
    await addFriendAsync(friendName.value).then((response) => {
        friendName.classList.remove('is-invalid');
        
    }).catch((e) => {
        friendName.classList.add('is-invalid');
        console.log('Friend not found');
        console.log(e);
        return;
    });
    fillFriendList();
    let addFriendModal = bootstrap.Modal.getInstance(document.getElementById('add-friend-modal'));
    addFriendModal.hide();
}