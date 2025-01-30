async function updateOverviewPage() {
    if (_user === null)
        _user = await getUserData();
    document.getElementById('username').innerText = `${i18next.t('overview.greeting')} ${_user?.username}`;
    document.getElementById('user-avatar').src = _avatar;
    document.getElementById('games-played').innerText = `${i18next.t('overview.gamesPlayed')}: ${_user?.games_played}`;
    document.getElementById('wins').innerText = `${i18next.t('overview.wins')}: ${_user?.wins}`;
    document.getElementById('losses').innerText = `${i18next.t('overview.losses')}: ${_user?.losses}`;
    document.getElementById('draws').innerText = `${i18next.t('overview.draws')}: ${_user?.draws}`;
    document.getElementById('pongPlayers').innerText = `${_user?.pong_players ?? 0} ${i18next.t('overview.playersPlaying')}`;
    document.getElementById('onlineFriends').innerText = `${_user?.online_friends ?? 0} ${i18next.t('overview.friendsOnline')}`;

    document.querySelectorAll('[data-i18n]').forEach(element => {
        let key = element.getAttribute('data-i18n');
        element.innerText = i18next.t(key);
    });
}