
async function getUserData() {
    const url = 'http://localhost:8080/api/users/1/'; //TODO Change to get correct user
    const response = await fetch(url);
    if (response.status !== 200) {
        console.error('Error fetching user data');
        return;
    };
    const data = await response.json();
    //TODO cache data
    return data;
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