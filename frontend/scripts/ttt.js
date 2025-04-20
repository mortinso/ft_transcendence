(function () {

	const board = document.getElementById('board');
	const message = document.getElementById('message');
	const resetButton = document.getElementById('reset');

	let currentPlayer = 'X';
	let gameActive = true;
	const gameState = Array(9).fill(null);

	const winningCombinations = [
		[0, 1, 2], [3, 4, 5], [6, 7, 8],
		[0, 3, 6], [1, 4, 7], [2, 5, 8],
		[0, 4, 8], [2, 4, 6]
	];

	function checkWinner() {
		for (const combination of winningCombinations) {
			const [a, b, c] = combination;
			if (gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
				return gameState[a];
			}
		}
		return gameState.includes(null) ? null : 'Tie';
	}

	async function SaveTTTStats(winner_){
		let winnerName = '';
		switch (winner_) {
			case 'X':
				winnerName = _user.username;
				break;
			case 'O':
				winnerName = i18next.t('games.player2');
				break;
			default:
				winnerName = 'tie';
		}
		await fetch(`/api/users/${_user.id}/games/create/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
			},
			body: JSON.stringify({
				winner: winnerName,
				draw: winnerName === 'tie' ? true : false,
				owner_won: winnerName === _user.username ? true : false,
				player1: _user.username,
				player2: i18next.t('games.player2'),
				result: "1x0",
				game_type: "TTT",
			})
		});
	}

	function handleClick(e) {
		const cell = e.target;
		const index = cell.dataset.index;

		if (!gameActive || gameState[index]) return;

		gameState[index] = currentPlayer;
		cell.textContent = currentPlayer;
		cell.classList.add('taken', currentPlayer);

		const winner = checkWinner();

		if (winner) {
			gameActive = false;
			let winnerName = winner === 'X' ? _user.username : i18next.t('games.player2');
			message.textContent = winner === 'Tie' ? i18next.t('games.tie') : `${i18next.t('games.player')} ${winnerName} ${i18next.t('games.wins')}`;
			SaveTTTStats(winner === 'Tie' ? 'tie' : currentPlayer).then(() => {});
		} else {
			currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
			let currentPlayerName = currentPlayer === 'X' ? _user.username : i18next.t('games.player2');
			message.textContent = `${i18next.t('games.playerTurn')}: ${currentPlayerName}`;
		}
	}

	function resetGame() {
		gameState.fill(null);
		currentPlayer = 'X';
		gameActive = true;
		let currentPlayerName = currentPlayer === 'X' ? _user.username : i18next.t('games.player2');
		message.textContent = `${i18next.t('games.playerTurn')}: ${currentPlayerName}`;
		board.innerHTML = '';
		createBoard();
	}

	function createBoard() {
		for (let i = 0; i < 9; i++) {
			const cell = document.createElement('div');
			cell.classList.add('cell');
			cell.dataset.index = i;
			cell.addEventListener('click', handleClick);
			board.appendChild(cell);
		}
	}

	resetButton.addEventListener('click', resetGame);
	createBoard();
	translateAll();

})();