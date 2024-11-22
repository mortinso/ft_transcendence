function updateProfilePage() {
    getUserData().then(user => {
        document.getElementById('username').innerText = `${user.username}`;
        createPongChart();
        createPongGameList();
        createSecondChart();
        createSecondGameList();
    });
}

//Create chart for pong games
function createPongChart() {
    new Chart("pongChart", {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                //TODO fetch data from backend
                data: [3, 2, 1],
                backgroundColor: ['green', 'red', 'grey']
            }]
        }
    })
}

//Create chart for the second game
function createSecondChart() {
    new Chart("secondChart", {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                //TODO fetch data from backend
                data: [5, 4, 2],
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