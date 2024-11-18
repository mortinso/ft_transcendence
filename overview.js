
async function getUserData() {
    const userID = getUserID();
    if (userID === null)
        return;
    const url = `http://localhost:8080/api/users/${userID}/`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            "Content-Type": "application/json",
            Authorization: `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (response.status !== 200) {
        console.error('Error fetching user data');
        return;
    };
    const data = await response.json();
    //TODO cache data
    return data;
}

function getUserID(){
    try {
        const payload = sessionStorage.getItem('jwt').split('.')[1];
        return JSON.parse(atob(payload))?.user_id;
    }
    catch (e) {
        return null;
    }
}

function updateOverviewPage() {
    getUserData().then(user => {
        console.log(user?.username, user);
        document.getElementById('username').innerText = `Hello ${user?.username}`;
        document.getElementById('games-played').innerText = `Games played: ${user?.games_played}`;
        document.getElementById('wins').innerText = `Wins: ${user?.wins}`;
        document.getElementById('losses').innerText = `Losses: ${user?.losses}`;
        document.getElementById('draws').innerText = `Draws: ${user?.draws}`;
        //document.getElementById('friends-online').innerText = `Friends online: ${user.friends_online}`;
    });
}