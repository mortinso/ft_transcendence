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
                data: [user?.pong_wins, user?.pong_losses, user?.pong_draws],
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

//Create list of last 5 games of pong
function createPongGameList() {
    //TODO fetch data from backend
    let testData = ["Won against test1", " Won against test2", " Lost against test3", "Draw against test4", "Lost against test5"];
    let gameList = document.getElementById('pongGameList');
    let template = document.getElementById("gameResultTemplate");
    let container = template.content.querySelector("a");
    testData.forEach(game => {
        let a = document.importNode(container, true);
        let img = a.querySelector("img");
        img.src = "https://avatars.githubusercontent.com/u/107864891?v=4";
        let h6 = a.querySelector("h6");
        h6.innerText = game;
        let p = a.querySelector("p");
        p.innerText = "Result: 0:0";
        let date = a.querySelector("small");
        date.innerText = "1min";
        new bootstrap.Tooltip(date, {
            title: "12:00 01.01.2024",
            placement: "top"
        });
        gameList.appendChild(a);
    });
}

//Create list of last 5 games of the second game
function createSecondGameList() {
    //TODO fetch data from backend
    let testData = ["Won against test1", " Won against test2", " Lost against test3", "Draw against test4", "Lost against test5"];
    let gameList = document.getElementById('secondGameList');
    let template = document.getElementById("gameResultTemplate");
    let container = template.content.querySelector("a");
    testData.forEach(game => {
        let a = document.importNode(container, true);
        let img = a.querySelector("img");
        img.src = "https://avatars.githubusercontent.com/u/107864891?v=4";
        let h6 = a.querySelector("h6");
        h6.innerText = game;
        let p = a.querySelector("p");
        p.innerText = "Result: 0:0";
        let date = a.querySelector("small");
        date.innerText = "1min";
        new bootstrap.Tooltip(date, {
            title: "12:00 01.01.2024",
            placement: "top"
        });
        gameList.appendChild(a);
    });
}