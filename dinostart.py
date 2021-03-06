import os
import sys
import time
import random
import pygame
from operator import itemgetter

BGCOLOR = (220,220,220)

jump = False
duck = False
animbool = False	
animboolbird1 = False
animboolbird2 = False
animboolduck = False
fpsCount = 0
pygame.mixer.pre_init(22050, -16, 1, 256)
pygame.mixer.init()
pygame.init()

fpscounter = 0



fps = 60 # this essentially decides how fast everything will be updating on the screen, need to test on a 60Hz screen as my screen with 144fps is a lot faster than it is with 60

# preload sound fx
collisionSound = pygame.mixer.Sound('./dinosprites/Explosion2.wav')
progressSound = pygame.mixer.Sound('./dinosprites/smw_message_block.wav')

lives = 3
global lives

class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        for i in range(0,6):
            try:
                img = pygame.image.load(os.path.join(imageinput+str(i)+'.png')).convert_alpha()
                # self.mask = pygame.mask.from_surface(self.image)
                # if pygame.sprite.spritecollide(b1, b2, False, pygame.sprite.collide_mask):
                #   print "sprites have collided!"
                self.images.append(img)
            except pygame.error as message:
                continue
        #img.convert_alpha()
        #img.set_colorkey(ALPHA)
       
        #alpha = 128
        #self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self.image = self.images[0]
        self.image.set_colorkey(BGCOLOR)
        self.rect = self.image.get_rect()

    def control(self, x, y):
        self.movex += x
        self.movey += y 
    def stop(self):
        self.movex = 0
        self.movey = 0
    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
    def duck(self):
        #self.rect = self.image.get_rect(y=660, x=125)
        #duckimg = pygame.image.load(os.path.join('./dinosprites/dinoduck.png')).convert_alpha()
        #self.images.append(duckimg)
        #self.image = self.images[3]
        #self.image.set_colorkey(BGCOLOR)
        global duck
        #duck = True
        global animboolduck
        if animboolduck == True:
            self.image = self.images[3]
            animboolduck = False
            return
        elif animboolduck == False:
            self.image = self.images[4]
            animboolduck = True
            return
        #self.rect = self.image.get_rect()
    def unduck(self):
        #self.rect = self.image.get_rect(y=625, x=125)
        self.image = self.images[0]
        self.image.set_colorkey(BGCOLOR)
        global duck
        duck = False
        player.rect.x = 175
        player.rect.y = 630
        #self.rect = self.image.get_rect()
    def animatedino(self):
        global animbool
        global duck
        if animbool == True and jump == False and duck == False:
            self.image = self.images[1]
            animbool = False
            return
        elif animbool == False and jump == False and duck == False:
            self.image = self.images[2]
            animbool = True
            return
        if jump == True:
            self.image = self.images[0]
        if duck == True:
            self.image = self.images[3]
    def animatebird1(self):
        global animboolbird1
        if animboolbird1 == True:
            self.image = self.images[0]
            animboolbird1 = False
            return
        elif animboolbird1 == False:
            self.image = self.images[1]
            animboolbird1 = True
            return
    def animatebird2(self):
        global animboolbird2
        if animboolbird2 == True:
            self.image = self.images[0]
            animboolbird2 = False
            return
        elif animboolbird2 == False:
            self.image = self.images[1]
            animboolbird2 = True
            return
    def jump(self, y):
        self.movey += y
        global jump
        jump = True
        player.animatedino()
    def randomcactus(self):
        cactusint = random.randint(0,2)
        self.image = self.images[cactusint]
        return

#ALPHA = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
worldx = 1920
worldy = 1080
screenBitDepth = 32
clock=pygame.time.Clock()
main = True
jumpcounter = 0

myfont = pygame.font.SysFont('Comic Sans MS', 64)
gameFont050 = pygame.font.Font('freesansbold.ttf', 050)
gameFont100 = pygame.font.Font('freesansbold.ttf', 100)
gameFont150 = pygame.font.Font('freesansbold.ttf', 150)
gameFont200 = pygame.font.Font('freesansbold.ttf', 200)

world = pygame.display.set_mode([worldx, worldy],pygame.FULLSCREEN,screenBitDepth)
pygame.mouse.set_visible(False)

imageinput = './dinosprites/properdino'
player = Object()
player.rect.x = 175
player.rect.y = 630
player_list = pygame.sprite.Group()
player_list.add(player)

imageinput = './dinosprites/bird'
enemy = Object()
enemy.rect.x = 1900
enemy.rect.y = 630 + random.randint(-275, -150)
enemy_list = pygame.sprite.Group() 
enemy_list.add(enemy)

imageinput = './dinosprites/bird'
flyingenemy = Object()
flyingenemy.rect.x = 1900
flyingenemy.rect.y = 630 + random.randint(-275, -150)
enemy_list.add(flyingenemy)

imageinput = './dinosprites/1stcactus'
cactusenemy = Object()
cactusenemy.rect.x = 1900
cactusenemy.rect.y = 630
enemy_list.add(cactusenemy)

cloudimage = pygame.image.load('./dinosprites/cloud_v10.png')
cloudrect = cloudimage.get_rect()

flyingenemyspawned = False

global enemyspeed
enemyspeed = random.randint(-7, -5)

global flyingenemyspeed
flyingenemyspeed = random.randint(-7, -5)

global cactusspeed
cactusspeed = random.randint(-13, -10)

global mainloop
mainloop = True

global collide
collide = False


starttime = time.time()

'''
def drawCloud(): 
    for i in range(4):  
        xsize = random.randint(40, 70)      
        ysize = random.randint(40, 70)
        size=random.randint(20,70)
        xOffset=random.randint(-40,40)
        yOffset=random.randint(-20,20)
        #pygame.draw.ellipse(world, BLACK, (100+xOffset, 100+yOffset, size, size), 0) # screen, color, (position, size), width
        pygame.draw.ellipse(world, BLACK, (1700, 250, 150, 60), 0)
        pygame.draw.ellipse(world, BLACK, (1675, 270, 165, 60), 0)
        #pygame.draw.ellipse(world, BGCOLOR, (1705, 255, 140, 70), 0)
'''

def message_display(text, size, xcenter, ycenter, updateDisplay):
    if (size==50):
        TextSurf, TextRect = text_objects(text, gameFont050)
    elif (size==100):
        TextSurf, TextRect = text_objects(text, gameFont100)
    elif (size==150):
        TextSurf, TextRect = text_objects(text, gameFont150)
    else:
        TextSurf, TextRect = text_objects(text, gameFont200)
    TextRect.center = (xcenter, ycenter)
    world.blit(TextSurf, TextRect)
    if (updateDisplay):
        # need to update the live display - game over overlay
        pygame.display.update(TextRect)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

global cloud1ypos
global cloud2ypos
cloud1ypos = 250+random.randint(-50,50)
cloud2ypos = 250+random.randint(-50,50)
global b
b = 0
global c
c = 0


def cloud():
    global b
    global c
    global cloud1ypos
    global cloud2ypos
    endtime = time.time()
    cloud1xpos = 2000-b 
    world.blit(cloudimage, (cloud1xpos, cloud1ypos))
    b += 3

    cloud2xpos = 2500-c
    if((endtime-starttime) > 5):
        world.blit(cloudimage, (cloud2xpos, cloud2ypos))
        c += 3
    if cloud1xpos < -125:
        b = 0
        cloudypos = 250+random.randint(-50,50)
    if cloud2xpos < -125:
        c = 500
        cloudypos = 250+random.randint(-50,50)

def refresh():
    global fpscounter
    global fpsCount
    fpscounter += 1
    fpsCount += 1
    world.fill((220,220,220))
    player.update()
    enemy.update()
    flyingenemy.update()
    cactusenemy.update()
    player_list.draw(world)
    enemy_list.draw(world)
    cloud()
    pygame.draw.line(world, (105, 105, 105), [150,700], [1770,700], 3)
    pygame.draw.rect(world, BGCOLOR, (0,0,150,1080), 0)
    pygame.draw.rect(world, BGCOLOR, (1770,0,150,1080), 0)
    if duck is True and (fpscounter % 8) == 0:
        player.duck()
    if((fpscounter % 8) == 0) and duck == False:
        player.animatedino()
    if(fpscounter % 15) == 0:
        enemy.animatebird1()
        flyingenemy.animatebird2()
    endtime = time.time()
    # display fps
    if (endtime > starttime):
        avgFps=int(fpsCount/(endtime-starttime))
        message_display('avgFps ' + str(avgFps), 50, 1700, 150, False)
    if collide is False:
        global score
        score = int((float("{0:.2f}".format(endtime-starttime))*10) * 1+float("{0:.2f}".format((endtime-starttime)/10)))
        #print 'score ' + str(score)
        message_display('Score ' + str(score), 50, 1700, 50, False)
        if score > 10 and (score % 98) == 0:
            progressSound.play()
    message_display('Lives: ' + str(lives), 50, 1690, 100, False)
    global flyingenemyspawned
    if flyingenemyspawned is False and endtime-starttime > 150:
        print 'random flying enemy spawned'
        flyingenemyspawned = True
    pygame.display.flip()
    clock.tick(fps)

def collisioncheck(sprite1, sprite2):
    collision = pygame.sprite.collide_rect(sprite1, sprite2)
    if collision == True:
        hit = False
        hit2 = False
        global lives
        if lives == 3: 
            lives += -1 
            #print lives
            var1 = fpscounter
            global var1
            collisionSound.play()
        if lives == 2:
            var2 = fpscounter
            if var2-var1 > 30 and hit == False:
                hit = True
                lives += -1
                var3 = fpscounter
                global var3
                collisionSound.play()
        if lives == 1:
            var4 = fpscounter
            if var4-var3 > 30 and hit2 == False:
                collisionSound.play()
                lives += -1
                global collide
                collide = True
                print "YOU LOSE!"
                global mainloop
                mainloop = False
                world.fill((220,220,220))
                enemy.stop()
                flyingenemy.stop()
                player.stop()   
                pygame.display.flip()
                refresh()
                message_display('Game Over', 100, 960, 300, True)
                message_display('Your Score: ' + str(score), 100, 960, 420, True)
                leaderboardfile = open("./leaderboard.txt", 'a')
                leaderboardfile.write(str(score) + ',' + str(jumpcounter) + '\n')
                leaderboardfile.close()
                leaderboardfile = open("./leaderboard.txt", 'r')
                lines = leaderboardfile.read().split('\n')
                lines.sort(key=itemgetter(0))
                del lines[0]
                print lines
                numScores = len(lines)+1
                playerrank = numScores
                for line in lines:# trying to make a leaderboard
                    #filespaceread = line.split(' ')
                    print line
                    #print filespaceread
                    if score > int(line[0]):
                        playerrank -= 1
                #message_display('Your Rank: ' + str(playerrank) + " out of " + str(numScores))

                time.sleep(5)

def reuseenemy():
    enemy.rect.x = 1900
    enemy.rect.y = 625 + random.randint(-275, -150)
    endtime = time.time()
    global enemyspeed
    attemptedspeed = (random.randint(-8, -1))-(int(endtime-starttime))/4
    if int(attemptedspeed) > -5:
        enemyspeed = random.randint(-8, -5)
    else:
        enemyspeed = attemptedspeed
    print str(enemyspeed) + ' enemy speed on respawn'

def reuseflyingenemy():
    flyingenemy.rect.x = 1900
    flyingenemy.rect.y = 625 + random.randint(-275, -150)
    endtime = time.time()
    global flyingenemyspeed 
    attemptedspeed = random.randint(-8, -1)-(int(endtime-starttime))/4
    if int(attemptedspeed) > -5:
        flyingenemyspeed = random.randint(-8, -5)
    else:
        flyingenemyspeed = attemptedspeed
    print str(flyingenemyspeed) + ' flyingenemy speed on respawn'


def reusecactus():
    cactusenemy.randomcactus()
    cactusenemy.rect.x = 2000
    cactusenemy.rect.y = 625
    endtime = time.time()
    global cactusspeed
    attemptedspeed = (random.randint(-8, -1))-(int(endtime-starttime))/4
    if int(attemptedspeed) > -5:
        cactusspeed = random.randint(-8, -6)
    else:
        cactusspeed = attemptedspeed
    print str(cactusspeed) + ' cactus speed speed on respawn'

starteventtime = 0
endeventtime = 0
while mainloop == True:
    for event in pygame.event.get():
        print (starteventtime-endeventtime)
        starteventtime = time.time()
        if starteventtime-endeventtime < 0.017: # this seems to work exactly how i want it to, you no longer can spam the keyboard and have it infinitely jump. Small enough delay that middle schoolers shouldn't notice.
            starteventtime = 100
            endeventtime = 0
        else:
            if event.type == pygame.KEYDOWN: #if a key is pressed
                print('key pressed')
                if event.key == pygame.K_DOWN:
                    print('down')
                    global duck 
                    duck = True
                    player.duck()
                    refresh()
                    player.rect.x = 175
                    player.rect.y = 655   
                    if collide == False:
                        collisioncheck(player, enemy)
                        collisioncheck(player, flyingenemy)
                        collisioncheck(player, cactusenemy)

                if event.key == pygame.K_UP:
                    print('up')
                    global duck
                    duck = False
                    player.unduck()
                    global jumpcounter
                    jumpcounter += 1
                    a = 23
                    #while a < 23 and collide == False:
                    while a > 0 and collide == False:
                        player.jump(-a)
                        enemy.control(enemyspeed, 0)
                        if flyingenemyspawned == True:
                            flyingenemy.control(flyingenemyspeed, 0)
                        cactusenemy.control(cactusspeed, 0)
                        refresh()
                        player.stop()
                        enemy.stop()
                        flyingenemy.stop()
                        cactusenemy.stop()
                        collisioncheck(player, enemy)
                        collisioncheck(player, flyingenemy)
                        collisioncheck(player, cactusenemy)
                        #clock.tick(fps)
                        a += -1      

                    a = 1
                    while a <= 23 and collide == False:
                        player.jump(a)
                        enemy.control(enemyspeed, 0)
                        if(flyingenemyspawned == True):
                            flyingenemy.control(flyingenemyspeed, 0)
                        cactusenemy.control(cactusspeed, 0)
                        refresh()
                        player.stop()
                        enemy.stop()
                        flyingenemy.stop()  
                        cactusenemy.stop()
                        collisioncheck(player, enemy)
                        collisioncheck(player, flyingenemy)
                        collisioncheck(player, cactusenemy)
                        #clock.tick(fps)
                        a += 1
                    jump = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.unduck()
                    player.rect.x = 175
                    player.rect.y = 630
                    if collide == False:
                        collisioncheck(player, enemy)
                        collisioncheck(player, flyingenemy)
                        collisioncheck(player, cactusenemy)

                if event.key == pygame.K_UP:
                    player.stop()
                    enemy.stop()
                    endeventtime = time.time()
                    global endeventtime
                    if collide == False:
                        collisioncheck(player, enemy)
                        collisioncheck(player, flyingenemy)
                        collisioncheck(player, cactusenemy)

                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    main = False

    endtime = time.time()
    timediff = endtime-starttime
    timedifftwo = float("{0:.2f}".format(timediff))
    timediffint = int(timediff)

    enemy.control(enemyspeed, 0)
    if(flyingenemyspawned == True):
        flyingenemy.control(flyingenemyspeed, 0)
    cactusenemy.control(cactusspeed, 0)

    refresh()
    enemy.stop()  
    flyingenemy.stop()
    cactusenemy.stop()

    if collide == False:
        collisioncheck(player, enemy)
        collisioncheck(player, flyingenemy)
        collisioncheck(player, cactusenemy)

    if enemy.rect.x < 0:
        reuseenemy()
    
    if cactusenemy.rect.x < 0:
        reusecactus()

    elif(flyingenemy.rect.x < 0) and ((timediffint % 8) == 0):
        print ' trying to spawn random flying enemy'
        if(((random.randint(2,10)) % 2) == 0):
            print  ' random flying enemy REUSED '
            reuseflyingenemy()

    '''
    #stay in the loop
    world.fill((220,220,220))
    pygame.draw.line(world, BLACK, [100,600], [1820,600], 3)
    #pygame.draw.rect(world, ALPHA, [250, 340, 20, 20])
    #print("player x: " + str(player.rect.x) + "player y: " + str(player.rect.y))
    player.update()
    player_list.draw(world)
    enemy.update()
    enemy_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
    '''
