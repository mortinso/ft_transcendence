(function () {
// Player bubble colors
const BUBBLE_COLORS = [
	'#c70b0b',	// Red
	'#ee940c',	// Orange
	'#1ca11c',	// Green
	'#0bb970',	// Teal
	'#1a70c0',	// Blue
	'#093875',	// Dark Blue
	'#502772',	// Purple
	'#e23ac6',	// Pink
];

let players = new Set();
let bracket, round, match, nextMatchPopup;

if(window.matchMedia("(pointer: coarse)").matches){
	document.getElementById('mobileWarning').classList.remove('d-none');
	document.getElementById('tournamentPage').classList.add('d-none');
}

function initTournament(playerNum) {
	if (!playerNum)
		return;
	let playerList = document.getElementById('playerList');
	let createButton = document.getElementById('createButton');
	let optionSection = document.getElementById('option-section');
	let playerSection = document.getElementById('player-section');

	playerList.textContent = '';

	// Set Player 1 to be the user
	const player1 = document.createElement('input');
	player1.id = 'player1';
	player1.className = 'player-name';
	getUserData().then(data => {  player1.value = data.username; });
	player1.readOnly = true;
	player1.style.borderColor = BUBBLE_COLORS[0];
	playerList.appendChild(player1);

	for (let i = 2; i <= playerNum; i++) {
		const player = document.createElement('input');
		player.id = `player${i}`;
		player.className = 'player-name';
		player.placeholder = `Player ${i}`;
		player.style.borderColor = BUBBLE_COLORS[(i - 1) % BUBBLE_COLORS.length];
		
		// Limit name length to 10 characters
        player.addEventListener('input', function () {
            if (player.value.length > 10)
                player.value = player.value.slice(0, 10);
        });
		
		playerList.appendChild(player);
	}

	optionSection.style.display = 'none';
	playerSection.style.display = 'block';
	createButton.onclick = function() { createTournament(`${playerNum}`); };
}

function checkNames(playerNum) {
	for (let i = 1; i <= playerNum; i++) {
		let username = document.getElementById(`player${i}`).value;
		if (!username)
			username = `Player ${i}`;
		if (players.has(username)) {
			alert(`No repeated names allowed: ${username}`);
			players.clear();
			return false;
		}
		players.add(username);
	}
	return true;
}

// Creates the tournament and its bracket
function createTournament(playerNum) {
	players.clear();
	if (!checkNames(playerNum))
		return;
	document.getElementById('newTournament').style.display = 'none';
	document.getElementById('player-section').style.display = 'none';

	bracket = document.getElementById('bracket');

	const rounds = Math.log2(playerNum) + 1;
	let matches = playerNum / 2;
	let playerArr = Array.from(players);

	arrayShuffle(playerArr);

	const spacer = document.createElement('li');
	spacer.className = 'spacer';
	spacer.innerHTML = '&nbsp;';

	const matchSpacer = document.createElement('li');
	matchSpacer.className = 'match match-spacer';
	matchSpacer.innerHTML = '&nbsp;';

	// Add all rounds to the bracket
	for (round = 1; round <= rounds; round++) {
		const roundElem = document.createElement('ul');
		roundElem.className = 'round';

		roundElem.appendChild(spacer.cloneNode(true));
		for (match = 0; round < rounds && match < matches; match++) {

			const player1 = document.createElement('li');
			player1.className = 'match player1';
			player1.dataset.round = round;
			player1.dataset.matchIndex = match;
			player1.dataset.position = 0;

			const player2 = document.createElement('li');
			player2.className = 'match player2';
			player2.dataset.round = round;
			player2.dataset.matchIndex = match;
			player2.dataset.position = 1;

			if (round == 1) {
				player1.textContent = playerArr[match * 2];
				player2.textContent = playerArr[match * 2 + 1];
			} else {
				player1.innerHTML = '<i class="tbd">TBD</i>';
				player2.innerHTML = '<i class="tbd">TBD</i>';
			}

			roundElem.appendChild(player1);
			roundElem.appendChild(matchSpacer.cloneNode(true));
			roundElem.appendChild(player2);
			roundElem.appendChild(spacer.cloneNode(true));
		}

		// This puts the winner section to the bracket
		if (round == rounds) {
			const winner = document.createElement('li');
			winner.className = 'match finalist';
			winner.innerHTML = '<i class="tbd">TBD</i>';
			winner.dataset.round = round;
			winner.dataset.matchIndex = 0;
			winner.dataset.position = 0;

			roundElem.appendChild(winner);
			roundElem.appendChild(spacer.cloneNode(true));
		}
		bracket.appendChild(roundElem);
		matches /= 2;
	}
	round = 1;
	match = 0;
	nextMatchPopup = document.getElementById("nextMatchPopup");
	nextMatchPopup.style.display = 'block';
	updateNextMatchPopup();
}

// Shuffles an array
function arrayShuffle(array) {
	for (let i = array.length - 1; i > 0; i--) {
	  const j = Math.floor(Math.random() * (i + 1));
	  [array[i], array[j]] = [array[j], array[i]];
	}
	return array;
}

// Starts the game of pong
function startGame(player1, player2) {
	document.getElementById('player1-title').innerHTML = `<span>${player1.innerText}</span>`;
	document.getElementById('player2-title').innerHTML = `<span>${player2.innerText}</span>`;
	
	bracket.style.display = 'none';
	nextMatchPopup.style.display = 'none';

	document.getElementById('game').style.display = 'block';

	playPong(player1, player2);
}

// Receives an element of the bracket and sets it to the winner of the match (if legal)
function selectWinner(element) {
	
	element.classList.add('winner');

	// Mark the match as decided
	document.querySelectorAll(`li[data-round="${round}"][data-match-index="${match}"]`).forEach(p => { p.classList.add('decided'); });
	
	const nextRoundElement = document.querySelector(`.round:nth-child(${round + 1})`);
	const nextPlayer = nextRoundElement.querySelector(`li[data-round="${round + 1}"][data-match-index="${Math.floor(match / 2)}"][data-position="${match % 2}"]`);
	
	// Update next instance of the player
	if (nextPlayer) {
		nextPlayer.innerHTML = element.textContent;
		if (nextPlayer.dataset.round > Math.log2(players.size)) {
			document.getElementById("tournamentWinnerPopup").style.display = 'block';

			document.getElementById("tournamentWinner").innerText = `${element.innerText} `;
			
			nextPlayer.classList.add("final-winner");
		}
	}
	
	calcNextMatch();
}

function calcNextMatch() {
	if (++match > ((players.size / (2 * round)) - 1)) {
		if (++round > Math.log2(players.size))
			return;
		match = 0;
	}

	nextMatchPopup.style.display = 'block';
	updateNextMatchPopup();
}

function updateNextMatchPopup() {
	const player1 = document.querySelector(`li[data-round="${round}"][data-match-index="${match}"][data-position="0"]`);
	const player2 = document.querySelector(`li[data-round="${round}"][data-match-index="${match}"][data-position="1"]`);
	
	document.getElementById("versusMessage").innerHTML= `${player1.innerText}&ensp;<b><i>VS</b></i>&ensp;${player2.innerText}`;

	// Remove previous event listeners and add the new one
	let playButton = document.getElementById("playButton");
	playButton.replaceWith(playButton.cloneNode(true));
	playButton = document.getElementById("playButton");
	playButton.addEventListener('click', function () { startGame(player1, player2); });
}

window.initTournament = initTournament;
window.selectWinner = selectWinner;

})();