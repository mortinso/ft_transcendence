let userProfile = null;

async function updateProfilePage(user=null) {
    if (user === null)
    {
        if (_user === null)
            _user = await getUserData();
    
        document.getElementById('username').innerText = `${_user?.username}`;
        document.getElementById('userAvatar').src = _avatar;
    }
    else
    {
        userProfile = await getUserByID(user);
        document.getElementById('username').innerText = `${userProfile?.username}`;
        if (userProfile?.avatar.includes('https%3A')){
            let avatar = userProfile.avatar.split('https%3A')[1];
            document.getElementById('userAvatar').src = `https:/${avatar}`;
            document.getElementById('userAvatar').style.objectFit = 'cover';
        }
        else
            document.getElementById('userAvatar').src = userProfile?.avatar;

        document.getElementById('add-friend-btn').classList.remove('d-none');
        if (_user.friends.includes(userProfile.id))
        {
            let btn = document.getElementById('add-friend-btn');
            btn.setAttribute('data-i18n', i18next.t('profile.removeFriend'));
            btn.classList.add('btn-danger');
            btn.onclick = () => changeContent('livechat');
        }
    }
    createPongChart();
    createPongGameList();
    createSecondChart();
    createSecondGameList();
    translateAll();
}

//Create chart for pong games
function createPongChart() {
    let user = userProfile === null ? _user : userProfile;
    new Chart("pongChart", {
        type: 'doughnut',
        data: {
            labels: [i18next.t('overview.wins'), i18next.t('overview.losses'), i18next.t('overview.draws')],
            datasets: [{
                data: [user?.pong_wins, user?.pong_losses],
                backgroundColor: ['green', 'red', 'grey']
            }]
        }
    })
}

//Create chart for the second game
function createSecondChart() {
    let user = userProfile === null ? _user : userProfile;
    new Chart("secondChart", {
        type: 'doughnut',
        data: {
            labels: [i18next.t('overview.wins'), i18next.t('overview.losses'), i18next.t('overview.draws')],
            datasets: [{
                data: [user?.ttt_wins, user?.ttt_losses, user?.ttt_draws],
                backgroundColor: ['green', 'red', 'grey']
            }]
        }
    })
}

async function getGameData() {
    let user = userProfile === null ? _user : userProfile;
    let gameData = await fetch(`/api/users/${user?.id}/games/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
        }
    });
    if (gameData.status !== 200) {
        return null;
    }
    return await gameData.json();
}

//Create list of pong games
async function createPongGameList() {
    let pongGames = await getGameData().then(data => {
        if (data === null) return null;
        let games = data.filter(game => game.game_type === "PONG");
        games.sort((a, b) => new Date(b.date) - new Date(a.date));
        return games;
    });
    let gameList = document.getElementById('pongGameList');
    let template = document.getElementById("gameResultTemplate");
    let container = template.content.querySelector("a");
    pongGames?.forEach(game => {
        let a = document.importNode(container, true);
        let h6 = a.querySelector("h6");
        h6.innerText = game.winner === _user.username ? `${i18next.t("games.wonAgainst")} ${game.player2}` : `${i18next.t("games.lostAgainst")} ${game.player2}`;
        let p = a.querySelector("p");
        p.innerText = `${i18next.t("games.result")}: ${game.result?.replace("x", ":")}`;
        let date = a.querySelector("small");
        const dateObj = new Date(game.date);
        let formattedDate = new Intl.DateTimeFormat(_lang).format(dateObj);
        if (Date.now() - dateObj.getTime() < 1000 * 60 * 60 * 24)
            formattedDate = new Intl.DateTimeFormat(_lang, { hour: '2-digit', minute: '2-digit' }).format(dateObj);
        date.innerText = `${formattedDate}`;
        new bootstrap.Tooltip(date, {
            title: `${new Intl.DateTimeFormat(_lang, {dateStyle: "medium", timeStyle:"medium"}).format(new Date(game.date))}`,
            placement: "top"
        });
        gameList.appendChild(a);
    });
}

//Create list of tic-tac-toe games
async function createSecondGameList() {
    let tttGames = await getGameData().then(data => {
        if (data === null) return null;
        let games = data.filter(game => game.game_type === "TTT");
        games.sort((a, b) => new Date(b.date) - new Date(a.date));
        return games;
    });
    let gameList = document.getElementById('secondGameList');
    let template = document.getElementById("gameResultTemplate");
    let container = template.content.querySelector("a");
    tttGames?.forEach(game => {
        let a = document.importNode(container, true);
        let h6 = a.querySelector("h6");
        switch (game.winner) {
            case game.player1:
                h6.innerText = `${i18next.t("games.wonAgainst")} ${game.player2}`;
                break;
            case game.player2:
                h6.innerText = `${i18next.t("games.lostAgainst")} ${game.player2}`;
                break;
            default:
                h6.innerText = `${i18next.t("games.drawAgainst")} ${game.player2}`;
        }
        let date = a.querySelector("small");
        const dateObj = new Date(game.date);
        let formattedDate = new Intl.DateTimeFormat(_lang).format(dateObj);
        if (Date.now() - dateObj.getTime() < 1000 * 60 * 60 * 24)
            formattedDate = new Intl.DateTimeFormat(_lang, { hour: '2-digit', minute: '2-digit' }).format(dateObj);
        date.innerText = `${formattedDate}`;
        new bootstrap.Tooltip(date, {
            title: `${new Intl.DateTimeFormat(_lang, {dateStyle: "medium", timeStyle:"medium"}).format(new Date(game.date))}`,
            placement: "top"
        });
        gameList.appendChild(a);
    });
}