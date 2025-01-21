(function() {

    const canvas = document.getElementById('pong');
    const ctx = canvas.getContext('2d');

    const PADDLE_SPEED = 2;
    const BALL_SPEED = 2;
    const SPEED_HITS = 5; //! mandatory

    const paddleWidth = 10;
    const paddleHeight = 100;
    const ballSize = 10;

    let ball = { x: canvas.width / 2, y: canvas.height / 2, vx: BALL_SPEED || 4, vy: BALL_SPEED || 4, hits: 0 };

    let player1 = { x: 0, y: canvas.height / 2 - paddleHeight / 2, score: 0, up: false, down: false };
    let player2 = { x: canvas.width - paddleWidth, y: canvas.height / 2 - paddleHeight / 2, score: 0, up: false, down: false };

    function drawRect(x, y, width, height, color) {
        ctx.fillStyle = color;
        ctx.fillRect(x, y, width, height);
    }

    function drawBall(x, y, size, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
    }

    function drawText(text, x, y, size = '20px') {
        ctx.fillStyle = 'white';
        ctx.font = `${size} Arial`;
        ctx.fillText(text, x, y);
    }

    function update() {
        // Ball movement
        ball.x += ball.vx;
        ball.y += ball.vy;

        // Ball collision with top and bottom walls
        if (ball.y < 0 || ball.y > canvas.height) {
            ball.vy *= -1;
        }

        // Ball collision with paddles
        if (
            ball.x <= player1.x + paddleWidth &&
            ball.y >= player1.y &&
            ball.y <= player1.y + paddleHeight
        ) {
            ball.vx *= -1;
            ball.hits++;
            checkSpeedIncrease();
        }

        if (
            ball.x >= player2.x - ballSize &&
            ball.y >= player2.y &&
            ball.y <= player2.y + paddleHeight
        ) {
            ball.vx *= -1;
            ball.hits++;
            checkSpeedIncrease();
        }

        // Ball out of bounds
        if (ball.x < 0) {
            player2.score++;
            resetBall();
        }

        if (ball.x > canvas.width) {
            player1.score++;
            resetBall();
        }

        // Player movement
        if (player1.up && player1.y > 0) player1.y -= PADDLE_SPEED || 5;
        if (player1.down && player1.y < canvas.height - paddleHeight) player1.y += PADDLE_SPEED || 5;

        if (player2.up && player2.y > 0) player2.y -= PADDLE_SPEED || 5;
        if (player2.down && player2.y < canvas.height - paddleHeight) player2.y += PADDLE_SPEED || 5;
    }

    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.vx = BALL_SPEED;
        ball.vy = BALL_SPEED;
        ball.hits = 0;
    }

    function checkSpeedIncrease() {
        if (ball.hits % SPEED_HITS === 0) {
            ball.vx *= 1.2;
            ball.vy *= 1.2;
        }
    }

    function draw() {
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw paddles
        drawRect(player1.x, player1.y, paddleWidth, paddleHeight, 'white');
        drawRect(player2.x, player2.y, paddleWidth, paddleHeight, 'white');

        // Draw ball
        drawBall(ball.x, ball.y, ballSize, 'white');

        // Draw scores
        drawText(player1.score, canvas.width / 4, 50);
        drawText(player2.score, (3 * canvas.width) / 4, 50);
    }

    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    window.addEventListener('keydown', (e) => {
        if (e.key === 'w') player1.up = true;
        if (e.key === 's') player1.down = true;
        if (e.key === 'ArrowUp') player2.up = true;
        if (e.key === 'ArrowDown') player2.down = true;
    });

    window.addEventListener('keyup', (e) => {
        if (e.key === 'w') player1.up = false;
        if (e.key === 's') player1.down = false;
        if (e.key === 'ArrowUp') player2.up = false;
        if (e.key === 'ArrowDown') player2.down = false;
    });

    gameLoop();
})();