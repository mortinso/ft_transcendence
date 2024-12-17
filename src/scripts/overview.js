async function updateOverviewPage() {
    if (_user === null)
        _user = await getUserData();
    document.getElementById('username').innerText = `Hello ${_user?.username}`;
    document.getElementById('user-avatar').src = _avatar;
    document.getElementById('games-played').innerText = `Games played: ${_user?.games_played}`;
    document.getElementById('wins').innerText = `Wins: ${_user?.wins}`;
    document.getElementById('losses').innerText = `Losses: ${_user?.losses}`;
    document.getElementById('draws').innerText = `Draws: ${_user?.draws}`;
    document.getElementById('friends-online').innerText = `Friends online: ${_user?.friends_online}`;
}