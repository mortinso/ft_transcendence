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
				player1: _user.username,
				player2: i18next.t('games.player2'),
				game_type: "ttt",
			})
		});
		//!Requires backend changes
		//TODO: update user stats
		/*
		await fetch(`/api/users/${_user.id}/edit/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
			},
			body: JSON.stringify({
				ttt_wins: winner === player1.name ? _user.ttt_wins + 1 : _user.ttt_wins,
				ttt_losses: winner === player2.name ? _user.ttt_losses + 1 : _user.ttt_losses,
				ttt_games_played: _user.ttt_games_played + 1,
			})
		});*/
		
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
			message.textContent = winner === 'Tie' ? i18next.t('games.tie') : `${i18next.t('games.player')} ${winner} ${i18next.t('games.wins')}`;
			SaveTTTStats(winner === 'Tie' ? 'tie' : currentPlayer).then(() => {});
		} else {
			currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
			message.textContent = `${i18next.t('games.playerTurn')}: ${currentPlayer}`;
		}
	}

	function resetGame() {
		gameState.fill(null);
		currentPlayer = 'X';
		gameActive = true;
		message.textContent = `${i18next.t('games.playerTurn')}: ${currentPlayer}`;
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