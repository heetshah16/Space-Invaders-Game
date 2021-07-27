import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo (1).png")
background = pygame.image.load("background.png")
pygame.display.set_icon(icon)
running = True
score = 0
font = pygame.font.Font('Signature Moments.ttf', 16)
font1 = pygame.font.Font("Shadow of the Deads.ttf", 45)
mixer.music.load("background.wav")
mixer.music.play(-1)
playerImg = pygame.image.load('player.png')
playerY = 480
playerX = 370
player_changeX = 0
player_changeY = 0

enemyImg = []
enemyY = []
enemyX = []
enemy_changeX = []
enemy_changeY = []

num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyY.append(random.randint(50, 150))
    enemyX.append(random.randint(0, 735))
    enemy_changeX.append(4)
    enemy_changeY.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletY = playerY
bulletX = playerX
bullet_changeX = 0
bullet_changeY = 10
bullet_state = "ready"


def show(x, y):
    scr = font.render("Score: " + str(score), True, (255, 225, 245))
    screen.blit(scr, (x, y))


def player(img, x=playerX, y=playerY):
    screen.blit(img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def IsCollision(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance <= 27:
        return True


def lose():
    sr = font1.render("GAME OVER ", True, (255, 225, 245))
    sr1 = font1.render("YOUR SCORE " + str(score), True, (255, 225, 245))
    screen.blit(sr, (200, 210))
    screen.blit(sr1, (200, 300))


while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    mixer.Sound.play(mixer.Sound("laser.wav"))
            if event.key == pygame.K_LEFT:
                player_changeX -= 5
            elif event.key == pygame.K_RIGHT:
                player_changeX += 5
            elif event.key == pygame.K_UP:
                player_changeY -= 5
            elif event.key == pygame.K_DOWN:
                player_changeY += 5
        elif event.type == pygame.KEYUP:
            player_changeY = 0
            player_changeX = 0
    playerX += player_changeX
    if bulletY == 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY
        if bulletY == 0:
            bulletY = playerY
            bullet_state = "ready"
    for i in range(num_of_enemy):
        if enemyY[i] >= 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            lose()
        player(enemyImg[i], enemyX[i], enemyY[i])
        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemy_changeX[i] = -enemy_changeX[i]
            enemyY[i] += enemy_changeY[i]
        if IsCollision(enemyX[i], bulletX, enemyY[i], bulletY):
            bulletY = playerY
            bullet_state = "ready"
            player(enemyImg[i], enemyX[i], enemyY[i])
            score += 1
            enemyY[i] = random.randint(50, 150)
            enemyX[i] = random.randint(0, 735)
            mixer.Sound.play(mixer.Sound("explosion.wav"))
    if playerX <= 0:
        playerX = 0
    if playerY <= 400:
        playerY = 400
    if playerX >= 736:
        playerX = 736
    if playerY >= 536:
        playerY = 536

    playerY += player_changeY
    show(10, 10)
    player(playerImg, playerX, playerY)
    pygame.display.update()
    lose()
