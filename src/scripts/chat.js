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