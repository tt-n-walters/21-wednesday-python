
import pygame
import time
import random
import os

folder = os.path.dirname(os.path.abspath(__file__))

pygame.init()



class Bullet:
    enemy = pygame.transform.rotate(pygame.image.load(folder + "/PNG/Lasers/laserRed07.png"), 180)
    player = pygame.image.load(folder + "/PNG/Lasers/laserBlue07.png")
    def __init__(self, x, y, friendly):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.friendly = friendly
    def move(self, x, y):
        self.x += x;
        self.y += y;
    def render(self, screen):
        if self.friendly:
            screen.blit(Bullet.player, (self.x, self.y))
        else:
            screen.blit(Bullet.enemy, (self.x, self.y))

class Spaceship:
    def __init__(self, x, y, lives):
        self.x = x;
        self.y = y;
        self.width = 100;
        self.height = 70;
        self.lives = lives;
        self.image = pygame.image.load(folder + "/PNG/playerShip2_orange.png")
        print(self.image)
    def move(self, x, y):
        self.x += x;
        self.y += y;
    def render(self, screen, shotTakenTime):
        
        timePassed = time.time()-shotTakenTime
        
        color = (100, 200, 100)
        
        if timePassed < 0.6:
            timePassed = round(timePassed, 1)
            if timePassed == 0.1 or timePassed == 0.3 or timePassed == 0.5:
                color = (255, 80, 80)
        
        screen.blit(self.image, (self.x, self.y))
class Alien:
    image1 = pygame.image.load(folder + "/PNG/Enemies/enemyBlue2.png")
    image2 = pygame.image.load(folder + "/PNG/Enemies/enemyRed2.png")
    image3 = pygame.image.load(folder + "/PNG/Enemies/enemyBlack2.png")
    def __init__(self, x, y, alien_type):
        self.x = x
        self.y = y
        self.width = 104
        self.height = 40
        self.alien_type = alien_type
    def move(self, x, y):
        self.x += x
        self.y += y
    def render(self, screen):
        image = Alien.image1
        if self.alien_type == 2:
            image = Alien.image2
        if self.alien_type == 3:
            image = Alien.image3
        screen.blit(image, (self.x, self.y))
class ShieldCell:
    def __init__(self, rx, ry, health, shield):
        self.rx = rx
        self.ry = ry
        self.width = 53
        self.height = 53
        self.health = health
        self.shield = shield
    def render(self, screen):
        color = (50, 200, 50)
        if self.health == 3:
            color = (200, 200, 50)
        if self.health == 2:
            color = (200, 100, 50)
        if self.health == 1:
            color = (200, 50, 50)
        pygame.draw.rect(screen, color, (self.shield.x+self.rx, self.shield.y+self.ry, self.width, self.height))
class Shield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = [
            ShieldCell(0, 0, 4, self),
            ShieldCell(0, 53, 4, self),
            ShieldCell(0, 105, 4, self),
            
            ShieldCell(53, 0, 4, self),
            ShieldCell(105, 0, 4, self),
            ShieldCell(158, 0, 4, self),
            
            ShieldCell(53, 53, 4, self),
            ShieldCell(105, 53, 4, self),
            ShieldCell(158, 53, 4, self),
            
            ShieldCell(158, 105, 4, self)
        ]
    def render(self, screen):
        for cell in self.cells:
            cell.render(screen)
def sortKey(elm):
    elmData = elm.split(":")
    return int(elmData[1])


pygame.font.init()

bigFont = pygame.font.SysFont("Arial", 80)
smallFont = pygame.font.SysFont("Arial", 40)
tinyFont = pygame.font.SysFont("Arial", 20)

lifeImage = pygame.image.load(folder + "/PNG/Power-ups/shield_bronze.png")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()

spaceX = 160            # Number of pixels per alien
spaceY = 120
aliensX = 6             # Number of aliens
aliensY = 3

aliens = []
bullets = []
shields = []
scoreTexts = []

lastTimeMoved = time.time()
lastTimeShot = time.time()
way = 1

score = 0

shieldNumber = 4
shieldSeparation = info.current_w/(shieldNumber)

for i in range(shieldNumber):
    shields.append(Shield((i+1)*shieldSeparation-shieldSeparation*3/4, info.current_h-250))

for i in range(aliensX):
    for j in range(aliensY):
        aliens.append(Alien(i*spaceX+54, j*spaceY+36, 3-j))


player1 = Spaceship(100, 0, 3)

player1.move(0, screen.get_height()-player1.height-20)

clock = pygame.time.Clock()

startScreen = True
done = False
endScreen = True

mainTitle = bigFont.render("Space Invaders", False, (200, 200, 200))
smallText = smallFont.render("Press 'enter' to start", False, (200, 200, 200))
playButtonText = smallFont.render("Play", False, (50, 50, 50))
quitButtonText = smallFont.render("Quit", False, (50, 50, 50))

mainTitleWidth = bigFont.size("Space Invaders")
smallTextWidth = smallFont.size("Press 'enter' to start")
playButtonTextWidth = smallFont.size("Play")
quitButtonTextWidth = smallFont.size("Quit")

name = "Unnamed"

playButtonWidth = 300
playButtonHeight = 100
playButtonY = 400
playButtonX = info.current_w/2-playButtonWidth/2
playButtonImage = pygame.image.load(folder + "/PNG/UI/green_button00.png")

quitButtonWidth = 300
quitButtonHeight = 100
quitButtonY = 550
quitButtonX = info.current_w/2-quitButtonWidth/2
quitButtonImage = pygame.image.load(folder + "/PNG/UI/red_button00.png")

while startScreen:
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.unicode != ':' and len(name) < 16:
                name += event.unicode
        
        if event.type == pygame.QUIT:
            startScreen = False
            done = True
    
    mainTitleX = info.current_w/2-mainTitleWidth[0]/2
    smallTextX = info.current_w/2-smallTextWidth[0]/2
    
    screen.fill((0, 0, 0))
    
    screen.blit(mainTitle, (mainTitleX, 100))
    #screen.blit(smallText, (smallTextX, 400))
    
    nameText = smallFont.render(name, False, (200, 200, 200))
    
    nameTextWidth = smallFont.size(name)
        
    screen.blit(nameText, (info.current_w/2-nameTextWidth[0]/2, 300))
    
    mouseCoords = pygame.mouse.get_pos()
    mousePressed = pygame.mouse.get_pressed()
    
    mouseX = mouseCoords[0]
    mouseY = mouseCoords[1]
    
    playButtonColor = (100, 200, 100)
    quitButtonColor = (200, 100, 100)
    
    if mouseX > playButtonX and mouseY > playButtonY and mouseX < playButtonX+playButtonWidth and mouseY < playButtonY+playButtonHeight:
        playButtonColor = (100, 255, 100)
        if mousePressed[0]:
            startScreen = False
    if mouseX > quitButtonX and mouseY > quitButtonY and mouseX < quitButtonX+quitButtonWidth and mouseY < quitButtonY+quitButtonHeight:
        quitButtonColor = (255, 100, 100)
        if mousePressed[0]:
            startScreen = False
            done = True
            endScreen = False
        
    # pygame.draw.rect(screen, playButtonColor, (playButtonX, playButtonY, playButtonWidth, playButtonHeight))
    # pygame.draw.rect(screen, quitButtonColor, (quitButtonX, quitButtonY, quitButtonWidth, quitButtonHeight))
    screen.blit(playButtonImage, (768 - 190/2, playButtonY + 25))
    screen.blit(quitButtonImage, (768 - 190/2, quitButtonY + 25))
    
    screen.blit(playButtonText, (playButtonX+playButtonWidth/2-playButtonTextWidth[0]/2, playButtonY+playButtonHeight/2-playButtonTextWidth[1]/2))
    screen.blit(quitButtonText, (quitButtonX+quitButtonWidth/2-quitButtonTextWidth[0]/2, quitButtonY+playButtonHeight/2-quitButtonTextWidth[1]/2))

    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_RETURN]:
        startScreen = False
    
    pygame.display.flip()

name = name.strip("\r")

startTime = time.time()

shotTakenTime = 0
    
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
            
    clock.tick(60)
        
    screen.fill((0, 0, 0))
    
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[pygame.K_a]:
        if player1.x >= 5:
            player1.move(-5, 0)
        
    if pressed_keys[pygame.K_d]:
        if player1.x <= screen.get_width()-player1.width-5:
            player1.move(5, 0)
    
    if pressed_keys[pygame.K_SPACE]:
        if time.time()-lastTimeShot > 0.7:
            bullets.append(Bullet(player1.x+player1.width/2-20, player1.y, True))
            bullets.append(Bullet(player1.x+player1.width/2+20, player1.y, True))
            lastTimeShot = time.time()
    
    for bullet in bullets:
        bullet.render(screen)
        if bullet.friendly:
            bullet.y -= 10
        else:
            bullet.y += 10
        if bullet.y < 0:
            bullets.remove(bullet)
        if bullet.y > info.current_h:
            bullets.remove(bullet)
        if bullet.x > player1.x and bullet.x < player1.x+player1.width and bullet.y > player1.y and bullet.y < player1.y+player1.height:
            if not bullet.friendly:
                player1.lives -= 1
                bullets.remove(bullet)
                score -= 15
                shotTakenTime = time.time()
                if player1.lives == 0:
                    done = True
                    
        for shield in shields:
            for cell in shield.cells:
                cellX = cell.rx+shield.x
                cellY = cell.ry+shield.y
                if bullet.x > cellX and bullet.x < cellX+cell.width and bullet.y > cellY and bullet.y < cellY+cell.height:
                    cell.health = cell.health - 1
                    if cell.health == 0:
                        shield.cells.remove(cell)
                    bullets.remove(bullet)
                    break
        
        for alien in aliens:
            playerRect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
            alienRect = pygame.Rect(alien.x, alien.y, alien.width, alien.height)
            if playerRect.colliderect(alienRect):
                player1.lives = 0
                done = True
            if bullet.x > alien.x and bullet.x < alien.x+alien.width and bullet.y > alien.y and bullet.y < alien.y+alien.height:
                if bullet.friendly:
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    
                    scoreValue = 10*alien.alien_type
                    score += scoreValue
                    scoreText = tinyFont.render("+"+str(scoreValue), False, (200, 200, 200))
                    scoreTexts.append({"scoreText": scoreText, "time": time.time(), "pos": alien})

                    if len(aliens) == 0:
                        done = True
                    break
    
    for scoreText in scoreTexts:
        if time.time()-scoreText["time"] > 0.5:
            scoreTexts.remove(scoreText)
        else:
            screen.blit(scoreText["scoreText"], (scoreText["pos"].x, scoreText["pos"].y))
    
    for alien in aliens:
        if random.randint(1, 10000) > 9999-600/len(aliens):
            bullets.append(Bullet(alien.x+alien.width/2, alien.y+alien.height, False))
        alien.render(screen)
        
    scoreText = smallFont.render("Score: "+str(score), False, (200, 200, 200))
    
    screen.blit(scoreText, (50, 50))

    for i in range(player1.lives):
        screen.blit(lifeImage, (info.current_w-60-i*60, 20))
    
    for shield in shields:
        shield.render(screen)
    
    if time.time()-lastTimeMoved > 0.6:
        
        newWay = way;
        for alien in aliens:
            alien.move(50*way, 0)
            if alien.x+alien.width > info.current_w:
                newWay = -1
            if alien.x-alien.width < 0:
                newWay = 1
        
        if way != newWay:
            for alien in aliens:
                alien.move(0, 30)
        way = newWay
        lastTimeMoved = time.time()
    
    player1.render(screen, shotTakenTime)
    
    pygame.display.flip()

timeTaken = time.time()-startTime
score = round(1000*score/timeTaken)    

finalText = "Game over!"
    
if len(aliens) == 0:
    finalText = "You won!"
    
endTitle = bigFont.render(finalText, False, (200, 200, 200))
endText = smallFont.render("Press 'q' to quit", False, (200, 200, 200))
scoreText = smallFont.render("Score: "+str(score), False, (200, 200, 200))

endTitleWidth = bigFont.size(finalText)
endTextWidth = smallFont.size("Press 'q' to quit")
scoreTextWidth = smallFont.size("Score: "+str(score))

f = open("scores.txt", "a")

f.write(name+": "+str(score)+"\n")

f.close()

f = open("scores.txt", "r")

scoreList = f.readlines()

f.close()

scoreList.sort(key=sortKey,reverse=True)

textList = []
for score in scoreList:
    textList.append(smallFont.render(score.strip("\n"), False, (200, 200, 200)))

while endScreen:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endScreen = False
    
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[pygame.K_q]:
        endScreen = False
        
    endTitleX = info.current_w/2-endTitleWidth[0]/2
    endTextX = info.current_w/2-endTextWidth[0]/2
    scoreTextX = info.current_w/2-scoreTextWidth[0]/2

    screen.fill((0,0,0))

    screen.blit(endTitle, (endTitleX, 100))
    screen.blit(endText, (endTextX, 400))
    screen.blit(scoreText, (scoreTextX, 200))
    
    scoreY = 450
    
    for text in textList:
        screen.blit(text, (500,scoreY))
        scoreY += 50
    
    pygame.display.flip()
    
pygame.quit()
