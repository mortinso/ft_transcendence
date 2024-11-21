
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
    if (response.status === 401) {
        if (sessionStorage.getItem('jwt') !== null && sessionStorage.getItem('refresh') !== null) {
            const refreshToken = sessionStorage.getItem('refresh');
            const url = 'http://localhost:8080/api/auth/api/token/refresh/';
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
                    return getUserData();
                }
                else {
                    return;
                }
            });
            return response;
        }
    }
    if (response.status !== 200) {
        console.error('Error fetching user data');
        logout();
        return;
    };
    const data = await response.json();
    //TODO cache data
    return data;
}

function getUserID() {
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