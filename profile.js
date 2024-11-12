function updateProfilePage(){
    getUserData().then(user => {
        console.log(user.username, user);
        document.getElementById('username').innerText = `${user.username}`;
        createPongChart();
        createPongGameList();
    });
}

function createPongChart(){
    new Chart("pongChart", {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                data: [3, 2, 1],
                backgroundColor: ['green', 'red', 'grey']
            }]
        }
    })
}

function createPongGameList(){
    let testData = ["test1", "test2", "test3"];
    let gameList = document.getElementById('pongGameList');
    temp = document.getElementById("gameResultTemplate");
    item = temp.content.querySelector("a");
    testData.forEach(game => {
        let a = document.importNode(item, true);
        a.innerText = game;
        gameList.appendChild(a);
    });
}