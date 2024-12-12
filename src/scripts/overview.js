function updateOverviewPage() {
    getUserData().then(user => {
        document.getElementById('username').innerText = `Hello ${user?.username}`;
        document.getElementById('games-played').innerText = `Games played: ${user?.games_played}`;
        document.getElementById('wins').innerText = `Wins: ${user?.wins}`;
        document.getElementById('losses').innerText = `Losses: ${user?.losses}`;
        document.getElementById('draws').innerText = `Draws: ${user?.draws}`;
        document.getElementById('friends-online').innerText = `Friends online: ${user?.friends_online}`;
        console.log(user);
    });
}