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
			message.textContent = winner === 'Tie' ? "It's a Tie!" : `Player ${winner} Wins!`;
		} else {
			currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
			message.textContent = `Player ${currentPlayer}'s turn`;
		}
	}

	function resetGame() {
		gameState.fill(null);
		currentPlayer = 'X';
		gameActive = true;
		message.textContent = "Player X's turn";
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

})();