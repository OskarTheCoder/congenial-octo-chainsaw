import pygame;
import random;
from pygame.locals import *;
import math;
import vectorMath;
pygame.init()
pygame.mouse.set_visible(True)

clock = pygame.time.Clock()
mapImg = pygame.image.load("graphics/map.png")

gameOver = False
levelComplete = False

def menu(screen, levelCompleted):
    inMenu = True

    levelCompletedFont = pygame.font.Font("fonts/futurist.ttf", 32)
    levelCompletedText = f"LEVEL {levelCompleted} COMPLETED"
    levelCompletedLabel = levelCompletedFont.render(levelCompletedText,True,((100,20,4)))
    levelCompletedTextPos = (352-levelCompletedLabel.get_width()//2,levelCompletedLabel.get_height()*2)

    continueLabel = levelCompletedFont.render("CONTINUE", True, ((100,20,4)) )
    continuePosLabel = (352-continueLabel.get_width()//2,200)

    continuePos = (352-250,200)
    continueRect = (continuePos[0],continuePos[1]-40,500,120)

    while(inMenu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                rect = pygame.Rect(continuePos[0],continuePos[1]-40,500,120)
                if rect.collidepoint(event.pos):
                    return 0
        screen.fill((255,255,255))
        screen.blit(levelCompletedLabel,levelCompletedTextPos)
        screen.blit(mapImg, (352-mapImg.get_width()//2,704-mapImg.get_height()-10))
        pygame.draw.rect(screen, ((122,122,122)), continueRect)
        screen.blit(continueLabel,continuePosLabel)
        pygame.display.update()

    return 0

class PLATFORM():
    def __init__(self,pos,speed,dir,active=False,min=-100,max=100):
        self.pos = pos
        self.speed = speed
        self.dir = dir
        self.img = pygame.image.load("graphics/platform.png")
        self.active = active
        self.PlayerStandingOn = False
        if (dir == "x"):
            self.min = self.pos[0]+min
            self.max = self.pos[0]+max
        else:
            self.min = self.pos[1]+min
            self.max = self.pos[1]+max
        self.switched = True

    def get_rect(self, Player):
        return self.img.get_rect(topleft=(self.pos[0],self.pos[1]))

    def move(self, Player, screen):
        if self.active:
            if self.dir == "x":
                if self.switched:
                    if self.PlayerStandingOn:
                        Player.movement[0]+=self.speed
                    self.pos[0]+=self.speed
                else:
                    if self.PlayerStandingOn:
                        Player.movement[0]-=self.speed
                    self.pos[0]-=self.speed
                if self.pos[0] > self.max or self.pos[0] < self.min:
                    self.switched = not self.switched
                


    def collision(self, screen, otherRect):
        if screen.getCollision(self.img.get_rect(topleft=(self.pos[0]+self.playerMovement[0]-(352-32),self.pos[1])), otherRect):
            return True
        return False


    def draw(self, screen, Player):
        screen.blit(self.img, (self.pos[0]-Player.movement[0]+352-32,self.pos[1]))

class PARTICLE():
    def __init__(self, color, width, radius, pos, velocities, lifetime, orgMovement):
        self.color = color
        self.width = width
        self.radius = radius
        self.orgPos = pos
        self.pos = pos
        self.velocities = velocities
        self.lifetime = lifetime
        self.orgMovement = orgMovement
    
    def draw(self, screen, Player):
        pygame.draw.circle(screen, (self.color), (self.pos[0]-(Player.movement[0]-self.orgMovement),self.pos[1]), self.radius, self.width)
        self.lifetime -= 1

    def move(self):
        self.pos[0] += self.velocities[0]
        self.pos[1] += self.velocities[1]


class GAMECLASS():
    def __init__(self, width, height, title):
        self.width = width
        self.height = height 
        self.title = title
        self.screen = 0
        self.bg = pygame.transform.scale( pygame.image.load("graphics/bgclouds.png") , (880, 570) )
        self.bgPos1 = [0,0]
        self.bgPos2 = [880,0]

    def setup(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def update(self, color):
        self.screen.fill(color)
        self.screen.blit(self.bg, (self.bgPos1[0], self.bgPos1[1]))
        self.screen.blit(self.bg, (self.bgPos2[0], self.bgPos2[1]))
        self.bgPos1[0] -= 0.5
        self.bgPos2[0] -= 0.5
        if (self.bgPos1[0]) <= -880:
            self.bgPos1[0] = 880
        elif (self.bgPos2[0]) <= -880:
            self.bgPos2[0] = 880

    
    def getKeyHeldDown(self, key):
        keys = pygame.key.get_pressed()
        if eval(f"keys[pygame.K_{key}]"):
            return True
        return False

    def getCollision(self, r1, r2):
        if pygame.Rect.colliderect(r1, r2):
            return True
        return False

    def getLevelData(self, level):
        dat = []
        with open(f"level{level}Data.txt", "r") as data:
            y = 0
            for row in data:
                dat.append([])
                for col in row.split(","):
                    dat[y].append(col)
                y+=1

            data.close()
        return dat


class PLAYER():
    def __init__(self, pos):
        self.idle = pygame.image.load("graphics/whiteBloodCell_Idle.png")
        self.runAnim = [pygame.image.load("graphics/whiteBloodCell_run2.png"),pygame.image.load("graphics/whiteBloodCell_run1.png"),pygame.image.load("graphics/whiteBloodCell_run3.png")]
        self.pos = pos
        self.image = self.idle
        self.weaponImage = pygame.image.load("graphics/weapon.png")
        self.running = False
        self.tick = 0
        self.dir = 0
        self.speed = 5
        self.flip = 1
        self.gravity = 2
        self.currentGravity = 0
        self.jumping = False
        self.movement = [352-32, 704-128]

    def getPos(self):
        return [self.pos[0], self.pos[1]]    

    def draw(self, screen):
        if (self.running==False):
            self.image = self.idle
        if (self.flip == 1):
            screen.blit(self.image, (self.pos[0], self.pos[1]))
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.pos[0], self.pos[1]))

    def move(self, screen, rects, particles, platforms):
        self.movement[0]+=self.dir*self.speed
        for rect in rects:
            if self.collision(screen, rect):      
                self.movement[0]-=self.dir*self.speed
                return False
        for platform in platforms:
            if self.collision(screen, platform.get_rect(self)):
                self.movement[0]-=self.dir*self.speed
                self.jumping = True
                self.currentGravity-=1
                return False
        for p in particles:
            pass

    def update(self, screen, rects, platforms):
        if self.running:
            self.tick += 6
        else:
            self.image = self.idle
        if self.tick != 0:
            if self.tick < 34:
                self.image = self.runAnim[0]
            elif self.tick < 67:
                self.image = self.runAnim[1]
            elif self.tick < 100:
                self.image = self.runAnim[2]
            else:
                self.tick = 0

        if self.jumping:
            if (self.pos[1] - self.currentGravity * self.gravity) > 704:
                self.jumping = False
                self.currentGravity = 0
                global gameOver
                gameOver = True
            else:
                self.pos[1] -= self.currentGravity * self.gravity
                for rect in rects:
                    if self.collision(screen, rect):
                        self.pos[1] += self.currentGravity * self.gravity
                        self.jumping = False
                        self.currentGravity = 0
                        return False
                for platform in platforms:
                    if self.collision(screen, platform.get_rect(self)) and platform.pos[1]-60 < self.pos[1]:
                        platform.PlayerStandingOn = True
                        self.pos[1] += self.currentGravity * self.gravity
                        self.jumping = False
                        self.currentGravity = 0
                        return False
                self.currentGravity -= 1

    def collision(self, screen, otherRect):
        if screen.getCollision(self.image.get_rect(center=(self.movement[0]+15,self.pos[1]+29)), otherRect):
            return True
        return False

    def checkIfStandingOnGround(self, screen, rects, platforms):
        if not self.jumping:
            self.pos[1] -= self.currentGravity * self.gravity
            for rect in rects:
                if self.collision(screen, rect):
                    self.pos[1] += self.currentGravity * self.gravity
                    return False     
            for platform in platforms:

                if self.collision(screen, platform.get_rect(self)) and platform.pos[1]-60 < self.pos[1]:
                    
                    self.pos[1] += self.currentGravity * self.gravity
                   
                    platform.PlayerStandingOn = True
                    
                    return False
                else:
                    pass
            self.jumping = True 
        return True

    def Input(self, screen,rects,platforms):
        keyPressed = False
        self.dir = 0
    
        if screen.getKeyHeldDown("d") or screen.getKeyHeldDown("RIGHT"):
            keyPressed = True
            self.dir = 1
            self.flip = 1
        if screen.getKeyHeldDown("a") or screen.getKeyHeldDown("LEFT"):
            if (keyPressed):
                self.dir = 0
                keyPressed = False
            else:
                self.dir = -1
                self.flip = -1
                keyPressed = True

        if keyPressed == False:
            self.running = False
        else:
            self.running = True

        if screen.getKeyHeldDown('SPACE') and self.currentGravity == 0 and self.jumping == False:
            self.currentGravity = -1
            if self.checkIfStandingOnGround(screen,rects,platforms) == False:
                self.currentGravity = 15
                self.jumping = True
    
    def rotateWeapon(self, screen):
        pos = pygame.mouse.get_pos()
        angle = 360-math.atan2(pos[1]-self.pos[1],pos[0]-self.pos[0])*180/math.pi
        rotimage = pygame.transform.rotate(self.weaponImage,angle)
        rect = rotimage.get_rect(center=(self.pos[0]+32,self.pos[1]+32))
        screen.blit(rotimage,rect)

class BULLET():
    def __init__(self, pos, dir, playerMovement, img):
        self.pos = pos 
        self.dir = dir
        self.speed = 15
        self.img = img
        self.playerMovement = playerMovement

    def move(self):
        self.pos[0] += self.speed * self.dir[0]
        self.pos[1] += self.speed * self.dir[1]
    
    def draw(self, screen):
        screen.blit(self.img, (self.pos[0],self.pos[1]))

    def collision(self, screen, otherRect):
        if screen.getCollision(self.img.get_rect(topleft=(self.pos[0]+self.playerMovement[0]-(352-32),self.pos[1])), otherRect):
            return True
        return False

GAME = GAMECLASS(704,704,"Game")
GAME.setup()

Player = PLAYER([352-32, 704-128])
bulletImg = pygame.image.load("graphics/bullet.png")
bullets = []
level = 1
levelData = GAME.getLevelData(level)
images = {"1": pygame.image.load("graphics/grass.png"),
          "3": pygame.image.load("graphics/ground.png"),
          "2": pygame.transform.scale( pygame.image.load("graphics/target.png"), (64,64) ),      
          "4": pygame.transform.scale( pygame.image.load("graphics/target_hit.png"), (64,64) ),      
          "5": pygame.image.load("graphics/flag_good.png"),
          "6": pygame.image.load("graphics/flag_shit.png"),
          "7": pygame.image.load("graphics/sand.png"),
          "8": pygame.image.load("graphics/sand_ground.png"),
          "9": pygame.image.load("graphics/platform.png"),
          "cactus": pygame.image.load("graphics/cactus.png"),
        }
rects = []
targetRect = 0
particles = []
trailParticles = []
platforms = []

if level ==1:
    flagRect = (images["5"].get_rect(topleft=(48*64,8*64)))
else:
    flagRect = 0

gameOverFont = pygame.font.Font("fonts/futurist.ttf", 64)
gameOverText = "game over"
gameOverLabel = gameOverFont.render(gameOverText, True, (170,0,0))
gameOverTextPos = (700//2 - (gameOverLabel.get_width()//2), 700//2-20 )

victoryFont = pygame.font.Font("fonts/fullpack.ttf", 32)
victoryFont2 = pygame.font.Font("fonts/fullpack.ttf", 16)
victoryText = "LEVEL COMPLETE"
victoryLabel = victoryFont.render(victoryText, True, (100,20,4))
victoryTextPos = [700//2 - (victoryLabel.get_width()//2), 700//2-50 ]
victoryTextSpawnPos = [-100-victoryLabel.get_width(), 700//2-50 ]
victoryTextSpawnPos2 = [800, 700//2-10 ]
victoryLabel2 = victoryFont.render("PRESS ANY BUTTON", False, (100,20,4))
victoryTextPos2 = [700//2 - (victoryLabel.get_width()//2), 700//2-10 ]

for y in range(len(levelData)):
    for x in range(len(levelData[0])):
        if levelData[y][x] == '1':
            rects.append(images["1"].get_rect(topleft=(x*64,y*64)))
        elif levelData[y][x] == '2':
            targetRect = images["2"].get_rect(topleft=(x*64,y*64))
        elif levelData[y][x] == '2':
            rects.append(images["2"].get_rect(topleft=(x*64,y*64)))
        elif levelData[y][x] == '3':
            rects.append(images["3"].get_rect(topleft=(x*64,y*64)))
        if levelData[y][x] == '7':
            rects.append(images["7"].get_rect(topleft=(x*64,y*64)))
        if levelData[y][x] == '8':
            rects.append(images["8"].get_rect(topleft=(x*64,y*64)))
        if levelData[y][x] == '9':
            if level == 2:
                platforms.append(PLATFORM([x*64,y*64],1,"x", False, 0,700))
        if levelData[y][x] == 'q':
            if level == 2:
                platforms.append(PLATFORM([x*64,y*64],1,"x", True, 0,700))
        if levelData[y][x] == 'c':
            rects.append(images["cactus"].get_rect(topleft=(x*64,y*64)))

running = False
while (running == False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            pos = pygame.mouse.get_pos()
            pos2 = Player.pos
            dirInAngles = vectorMath.calculateDirectionInRadians(pos2,pos)+math.radians(90)
            dirX = math.sin(dirInAngles)
            dirY = math.cos(dirInAngles)
            dir = [dirX,-dirY]
            positionToSpawn = Player.getPos()
            positionToSpawn[0] += 24
            positionToSpawn[1] += 16
            angle = 360-math.atan2(pos[1]-positionToSpawn[1],pos[0]-positionToSpawn[0])*180/math.pi
            rotimage = pygame.transform.rotate(bulletImg,angle)
            bullets.append(BULLET(positionToSpawn, dir, Player.movement, rotimage))
        if event.type == pygame.KEYDOWN and levelComplete:
            if menu(GAME.screen, level-1) != 0:
                running = True
                break
            levelComplete = False
            levelData = GAME.getLevelData(level)
            particles = []
            flagRect = 0
            rects = []
            for y in range(len(levelData)):
                for x in range(len(levelData[0])):
                    if levelData[y][x] == '1':
                        rects.append(images["1"].get_rect(topleft=(x*64,y*64)))
                    elif levelData[y][x] == '2':
                        targetRect = images["2"].get_rect(topleft=(x*64,y*64))
                    elif levelData[y][x] == '2':
                        rects.append(images["2"].get_rect(topleft=(x*64,y*64)))
                    elif levelData[y][x] == '3':
                        rects.append(images["3"].get_rect(topleft=(x*64,y*64)))
                    if levelData[y][x] == '7':
                        rects.append(images["7"].get_rect(topleft=(x*64,y*64)))
                    if levelData[y][x] == '8':
                        rects.append(images["8"].get_rect(topleft=(x*64,y*64)))
                    if levelData[y][x] == '9':
                        if level == 2:
                            platforms.append(PLATFORM([x*64,y*64],1,"x", False, 0,700))
                    if levelData[y][x] == 'q':
                        #if level == 2:
                        platforms.append(PLATFORM([x*64,y*64],1,"x", True, -100,700))
                    if levelData[y][x] == 'c':
                        rects.append(images["cactus"].get_rect(topleft=(x*64,y*64)))


            trailParticles = []
            Player.pos = [352-32, 704-128]
            Player.movement = [352-32,0]
            if level == 2:
                flagRect = 0

    GAME.update((78,173,245))
    for y in range(len(levelData)):
        for x in range(len(levelData[0])):
            if levelData[y][x] == '1':
                GAME.screen.blit(images["1"], (x*64-Player.movement[0]+352-32,y*64))
            elif levelData[y][x] == '2':
                GAME.screen.blit(images["2"], (x*64-Player.movement[0]+352-32,y*64))
            elif levelData[y][x] == '3':
                GAME.screen.blit(images["3"], (x*64-Player.movement[0]+352-32,y*64))
            elif levelData[y][x] == '4':
                GAME.screen.blit(images["4"], (x*64-Player.movement[0]+352-32,y*64))     
            elif levelData[y][x] == '5':
                GAME.screen.blit(images["5"], (x*64-Player.movement[0]+352-32,y*64))      
            elif levelData[y][x] == '6':
                GAME.screen.blit(images["6"], (x*64-Player.movement[0]+352-32,y*64))
            elif levelData[y][x] == '7':
                GAME.screen.blit(images["7"], (x*64-Player.movement[0]+352-32,y*64))
            elif levelData[y][x] == '8':
                GAME.screen.blit(images["8"], (x*64-Player.movement[0]+352-32,y*64))

    for p in trailParticles:
        if p.lifetime <= 0:
            trailParticles.remove(p)
        else:
            p.move()
            p.draw(GAME.screen, Player)



    if (gameOver==False):
        if (not levelComplete):
            Player.Input(GAME, rects, platforms)
            Player.checkIfStandingOnGround(GAME, rects,platforms)

            Player.move(GAME, rects, particles, platforms)
            Player.update(GAME, rects, platforms)
            
            if Player.currentGravity < -1 or Player.currentGravity > 0:
                for platform in platforms:
                    platform.PlayerStandingOn = False
        else:
            Player.image = Player.idle
        Player.draw(GAME.screen)

    for p in particles:
        if p.lifetime <= 0:
            particles.remove(p)
        else:
            p.move()
            p.draw(GAME.screen, Player)

    for p in platforms:
        p.move(Player, GAME)
        p.draw(GAME.screen,Player)

    if (not levelComplete):
        for bullet in bullets:
            if bullet.pos[0] < -2000 or bullet.pos[1] < -2000 or bullet.pos[1] > 2704 or bullet.pos[0] > 704:
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw(GAME.screen)
                if flagRect != 0:
                    if bullet.collision(GAME, flagRect):
                        levelData[8][48] = "5"
                        levelComplete = True
                        level+=1
                        bullets.remove(bullets[bullets.index(bullet)])
                        break
                for rect in rects:
                    if bullet.collision(GAME, rect):
                        bullets.remove(bullets[bullets.index(bullet)])
                        a = [random.randint(-20, 20) / 20,random.randint(-20, 20) / 20]
                        particles.append(PARTICLE((136, 42, 3), 3, 6, [bullet.pos[0],bullet.pos[1]], a, 50, Player.movement[0]))
                        b = [random.randint(-22, 22) / 24,random.randint(-22, 22) / 24]
                        particles.append(PARTICLE((136, 42, 3), 2, 5, [bullet.pos[0],bullet.pos[1]], b, 50, Player.movement[0]))

                        print(a,b)

                        break
                    if targetRect != 0:
                        if bullet.collision(GAME, targetRect):
                            bullets.remove(bullets[bullets.index(bullet)])

                            levelData[4][3] = '4'
                            if level == 1:
                                levelData[7][11] = '1'
                                rects.append(images["1"].get_rect(topleft=(11*64,7*64)))
                                levelData[7][12] = '1'
                                rects.append(images["1"].get_rect(topleft=(12*64,7*64)))
                                levelData[7][13] = '1'
                                rects.append(images["1"].get_rect(topleft=(13*64,7*64)))
                                levelData[7][14] = '1'
                                rects.append(images["1"].get_rect(topleft=(14*64,7*64)))
                                levelData[7][15] = '1'
                                rects.append(images["1"].get_rect(topleft=(15*64,7*64)))
                                levelData[7][16] = '1'
                                rects.append(images["1"].get_rect(topleft=(16*64,7*64)))
                            elif level == 2:
                                levelData[9][16] = '4'
                                platforms[0].active = True
                            break       

    if (gameOver):
        GAME.screen.blit(gameOverLabel, gameOverTextPos)#;
    if (levelComplete):
        GAME.screen.blit(victoryLabel, victoryTextSpawnPos)#;
        if victoryTextSpawnPos != victoryTextPos:
            dif = victoryTextPos[0]-victoryTextSpawnPos[0]
            victoryTextSpawnPos[0]+=dif/50
        GAME.screen.blit(victoryLabel2, victoryTextSpawnPos2)#;
        if victoryTextSpawnPos2 != victoryTextPos2:
            dif = victoryTextPos2[0]-victoryTextSpawnPos2[0]
            victoryTextSpawnPos2[0]+=dif/50

    #if Player.dir != 0:
    #    trailParticles.append(PARTICLE((255,255,255), 1, 1, [Player.pos[0]+Player.image.get_width()/2,Player.pos[1]+Player.image.get_height()/2], [random.random()/10,random.random()/10],120,Player.movement[0]))

    pygame.display.update()
    clock.tick(30)



