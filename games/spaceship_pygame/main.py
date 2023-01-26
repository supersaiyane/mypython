import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init();

#create a screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('galaxy.jpg')

#background sound 
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX=370
playerY=480
playerX_change=0

#single enemy
# enemyImg = pygame.image.load('enemy.png')
# # using random for changing position of enemy
# enemyX=random.randint(0,735)
# enemyY=random.randint(50,150)
# enemyX_change=0.3
# enemyY_change=40


#multiple Enemies
enemyImg = []
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(50)



#single bullet
bulletImg = pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=0.9
#ready = yu can't see the bullet on the screen
#fire = bullet is moving
bullet_state="ready"


#score font
scoreValue = 0
font =  pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game over font
over_font = pygame.font.Font('freesansbold.ttf',64)

def showScore(x,y):
    score = font.render("Score : " + str(scoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

#single enemy
# def enemy(x,y):
#     screen.blit(enemyImg,(x,y))    

#multiple enemy
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))     

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    #to find the distance between bullet and enemy, we have to user their x and y coordinates
    #https://www.mathsisfun.com/algebra/distance-2-points.html
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False



#game loop
running= True
while running:
    #RGB fillouts 
    screen.fill((0,0,0))
    #load background image
    screen.blit(background,(0,0))
    #playerY -= 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #check keypress events for our spaceship
        # x ----
        # y |
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print("left down")
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                #print("right down")
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    #get the current x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    #setting boundries for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    #setting boundries for one enmy
    # enemyX += enemyX_change
    # if enemyX <= 0:
    #     enemyX_change = 0.1
    #     enemyY += enemyY_change
    # elif enemyX >= 736:
    #     enemyX_change = -0.1
    #     enemyY += enemyY_change

    #setting boundries for multiple enmy
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.1
            enemyY[i] += enemyY_change[i]

        #collision for multiple enemy
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreValue += 1
            #print(score)
            #reEngaegEnemy()
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)  

        enemy(enemyX[i],enemyY[i],i)

    #bullet
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    #collision for one enemy
    # collision = isCollision(enemyX,enemyY,bulletX,bulletY)
    # if collision:
    #     bulletY = 480
    #     bullet_state = "ready"
    #     score += 1
    #     print(score)
    #     #reEngaegEnemy()
    #     enemyX=random.randint(0,735)
    #     enemyY=random.randint(50,150)

    player(playerX,playerY)
    #single enemy
    #enemy(enemyX,enemyY)
    showScore(textX,textY)
    pygame.display.update()