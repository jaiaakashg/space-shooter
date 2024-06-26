#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from IPython.display import display, HTML

display(HTML('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Advanced Space Shooter</title>
<style>
    body {
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #000;
    }
    canvas {
        border: 1px solid #fff;
        background-color: #000;
    }
    .scoreboard, .health {
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: #fff;
        font-size: 24px;
    }
    .health {
        top: 40px;
    }
</style>
</head>
<body>
<div class="scoreboard" id="scoreboard">Score: 0</div>
<div class="health" id="health">Health: 3</div>
<canvas id="gameCanvas" width="600" height="400"></canvas>
<script>
    const canvas = document.getElementById('gameCanvas');
    const context = canvas.getContext('2d');
    const scoreboard = document.getElementById('scoreboard');
    const healthDisplay = document.getElementById('health');

    const player = { width: 40, height: 40, x: canvas.width / 2 - 20, y: canvas.height - 50, speed: 5, health: 3 };
    const bullets = [];
    const enemies = [];
    const powerUps = [];
    let score = 0;
    let gameOver = false;

    function drawPlayer() {
        context.fillStyle = '#0f0';
        context.beginPath();
        context.moveTo(player.x + player.width / 2, player.y);
        context.lineTo(player.x, player.y + player.height);
        context.lineTo(player.x + player.width, player.y + player.height);
        context.closePath();
        context.fill();
    }

    function drawBullets() {
        context.fillStyle = '#ff0';
        for (const bullet of bullets) {
            context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        }
    }

    function drawEnemies() {
        context.fillStyle = '#f00';
        for (const enemy of enemies) {
            context.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        }
    }

    function drawPowerUps() {
        context.fillStyle = '#0ff';
        for (const powerUp of powerUps) {
            context.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
        }
    }

    function updateBullets() {
        for (let i = 0; i < bullets.length; i++) {
            bullets[i].y -= bullets[i].speed;
            if (bullets[i].y < 0) {
                bullets.splice(i, 1);
                i--;
            }
        }
    }

    function updateEnemies() {
        for (let i = 0; i < enemies.length; i++) {
            enemies[i].y += enemies[i].speed;
            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
                i--;
                player.health--;
                updateHealth();
                if (player.health <= 0) {
                    gameOver = true;
                }
            }
        }

        if (Math.random() < 0.05) {
            enemies.push({
                x: Math.random() * (canvas.width - 20),
                y: 0,
                width: 20,
                height: 20,
                speed: 2 + Math.random() * 3
            });
        }
    }

    function updatePowerUps() {
        for (let i = 0; i < powerUps.length; i++) {
            powerUps[i].y += powerUps[i].speed;
            if (powerUps[i].y > canvas.height) {
                powerUps.splice(i, 1);
                i--;
            }
        }

        if (Math.random() < 0.01) {
            powerUps.push({
                x: Math.random() * (canvas.width - 20),
                y: 0,
                width: 20,
                height: 20,
                speed: 2,
                effect: 'health'
            });
        }
    }

    function checkCollisions() {
        for (let i = 0; i < bullets.length; i++) {
            for (let j = 0; j < enemies.length; j++) {
                if (isColliding(bullets[i], enemies[j])) {
                    bullets.splice(i, 1);
                    enemies.splice(j, 1);
                    score++;
                    updateScoreboard();
                    i--;
                    break;
                }
            }
        }

        for (let i = 0; i < powerUps.length; i++) {
            if (isColliding(player, powerUps[i])) {
                if (powerUps[i].effect === 'health') {
                    player.health++;
                    updateHealth();
                }
                powerUps.splice(i, 1);
                i--;
            }
        }
    }

    function isColliding(rect1, rect2) {
        return !(rect1.x > rect2.x + rect2.width || rect1.x + rect1.width < rect2.x || rect1.y > rect2.y + rect2.height || rect1.y + rect1.height < rect2.y);
    }

    function updateScoreboard() {
        scoreboard.textContent = `Score: ${score}`;
    }

    function updateHealth() {
        healthDisplay.textContent = `Health: ${player.health}`;
    }

    function gameLoop() {
        if (gameOver) {
            context.fillStyle = '#fff';
            context.font = '24px Arial';
            context.fillText('Game Over', canvas.width / 2 - 50, canvas.height / 2);
            return;
        }

        context.clearRect(0, 0, canvas.width, canvas.height);
        drawPlayer();
        drawBullets();
        drawEnemies();
        drawPowerUps();
        updateBullets();
        updateEnemies();
        updatePowerUps();
        checkCollisions();
        requestAnimationFrame(gameLoop);
    }

    canvas.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        player.x = event.clientX - rect.left - player.width / 2;
        player.y = event.clientY - rect.top - player.height / 2;
        if (player.x < 0) player.x = 0;
        if (player.x > canvas.width - player.width) player.x = canvas.width - player.width;
        if (player.y < 0) player.y = 0;
        if (player.y > canvas.height - player.height) player.y = canvas.height - player.height;
    });

    window.addEventListener('keydown', function(event) {
        if (event.key === ' ') {
            bullets.push({
                x: player.x + player.width / 2 - 2.5,
                y: player.y,
                width: 5,
                height: 10,
                speed: 7
            });
        }
    });

    updateScoreboard();
    updateHealth();
    gameLoop();
</script>
</body>
</html>
'''))

