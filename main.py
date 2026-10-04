from array import array
import math
import random
import pygame

# Constants
SW = 800
SH = 500
PSX = 370
PSY = 380
ESYMIN = 50
ESYMAX = 150
ESX = 2
ESY = 20
BSY = 10

# Initialization
pygame.init()
screen = pygame.display.set_mode((SW, SH))
background = pygame.image.load('space.png')
pygame.display.set_caption("space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Hit sound
def create_hit_sound():
    sample_rate, _, channels = pygame.mixer.get_init()
    samples = array('h')
    for note in (659, 784):
        note_length = int(sample_rate * 0.12)
        for i in range(note_length):
            envelope = min(1, i / (sample_rate * 0.01), (note_length - i) / (sample_rate * 0.02))
            sample = int(12000 * math.sin(2 * math.pi * note * i / sample_rate) * envelope)
            samples.extend([sample] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())

hit_sound = create_hit_sound()

# Player Setup
playerImg = pygame.image.load('player.png')
playerX = PSX
playerY = PSY
playerX_change = 0

# Enemy Setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, SW - 64))
    enemyY.append(random.randint(ESYMIN, ESYMAX))
    enemyX_change.append(ESX)
    enemyY_change.append(ESY)

# Bullet Setup
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = PSY
bulletY_change = BSY
bullet_state = "ready"

# Score & Fonts
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27

# Main Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                
        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerX_change = 0

    # Player Movement Boundaries
    playerX += playerX_change
    playerX = max(0, min(playerX, SW - 64))
    
    # Enemy Mechanics Loop
    for i in range(num_of_enemies):
        # Game Over Condition
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Move Enemy
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= SW - 64:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
            
        # Collision Handling
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = PSY
            bullet_state = "ready"
            score_value += 1  # Fixed: now properly adds to score
            hit_sound.play()
            enemyX[i] = random.randint(0, SW - 64)
            enemyY[i] = random.randint(ESYMIN, ESYMAX)
            
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement Logic (Fixed positioning and flow)
    if bulletY <= 0:
        bulletY = PSY
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Render Screen Elements
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

