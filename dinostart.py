import os
import sys
import time
import random
import pygame
# testing git
class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join(imageinput)).convert_alpha()
        #img.convert_alpha()
        #img.set_colorkey(ALPHA)
        self.images.append(img)
        #alpha = 128
        #self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self.image = self.images[0]
        self.image.set_colorkey((220,220,220))
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
    def jump(self, y):
        self.movey += y
    def duck(self):
        self.rect = self.image.get_rect(y=560, x=125)
    def unduck(self):
        self.rect = self.image.get_rect(y=525, x=125)

#ALPHA = (0, 255, 0)
BLACK = (0, 0, 0)
worldx = 1920
worldy = 1080
fps = 60 # this essentially decides how fast everything will be updating on the screen, need to test on a 60Hz screen as my screen with 144fps is a lot faster than it is with 60
clock=pygame.time.Clock()
pygame.init()
main = True

myfont = pygame.font.SysFont('Comic Sans MS', 64)
world = pygame.display.set_mode([worldx, worldy])
imageinput = './dinosprites/properdino.png'
player = Object()
player.rect.x = 125
player.rect.y = 525
player_list = pygame.sprite.Group()
player_list.add(player)

imageinput = './dinosprites/rsz_rsz_1googleenemy.png'
enemy = Object()
enemy.rect.x = 1900
enemy.rect.y = 525 + random.randint(-120, 20)
enemy_list = pygame.sprite.Group()
enemy_list.add(enemy)

imageinput = './dinosprites/rsz_rsz_1googleenemy.png'
flyingenemy = Object()
flyingenemy.rect.x = 1900
flyingenemy.rect.y = 525 + random.randint(-120, 20)
enemy_list.add(flyingenemy)

imageinput = './dinosprites/1stcactus.png'
cactusenemy = Object()
cactusenemy.rect.x = 1900
cactusenemy.rect.y = 525
enemy_list.add(cactusenemy)

textsurface = myfont.render('GAME OVER YOU LOSE', False, BLACK)

global flyingenemyspawned
flyingenemyspawned = False

global enemyspeed
enemyspeed = random.randint(-12, -7)

global flyingenemyspeed 
flyingenemyspeed = random.randint(-12, -7)

global cactusspeed
cactusspeed = random.randint(-12, -9)

global mainloop
mainloop = True

global collide
collide = False

starttime = time.time()

def message_display(text, size, xcenter, ycenter):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (xcenter, ycenter)
    world.blit(TextSurf, TextRect)
    pygame.display.update(TextRect)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def refresh():
    world.fill((220,220,220))
    player.update()
    enemy.update()
    flyingenemy.update()
    cactusenemy.update()
    player_list.draw(world)
    enemy_list.draw(world)
    pygame.draw.line(world, BLACK, [100,600], [1820,600], 3)
    endtime = time.time()
    if collide == False:
        global score
        score = int((float("{0:.2f}".format(endtime-starttime))*10) * 1+float("{0:.2f}".format((endtime-starttime)/10)))
        #print 'score ' + str(score)
        message_display('Score ' + str(score), 48, 1700, 150)
    pygame.display.flip()
    clock.tick(fps)

def collisioncheck(sprite1, sprite2):
    collision = pygame.sprite.collide_rect(sprite1, sprite2)
    if collision == True:
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
        message_display('Game Over', 115, 960, 300)
        message_display('Your Score: ' + str(score), 60, 960, 420)
        time.sleep(5)

def reuseenemy():
    enemy.rect.x = 1900
    enemy.rect.y = 525 + random.randint(-60, 20)
    endtime = time.time()
    global enemyspeed
    attemptedspeed = (random.randint(-8, -1))-(int(endtime-starttime))/6
    if int(attemptedspeed) > -5:
        enemyspeed = random.randint(-8, -5)
    else:
        enemyspeed = attemptedspeed
    print str(enemyspeed) + ' enemy speed on respawn'

def reuseflyingenemy():
    flyingenemy.rect.x = 1900
    flyingenemy.rect.y = 525 + random.randint(-60, 20)
    endtime = time.time()
    global flyingenemyspeed 
    attemptedspeed = random.randint(-8, -1)-(int(endtime-starttime))/6
    if int(attemptedspeed) > -5:
        flyingenemyspeed = random.randint(-8, -5)
    else:
        flyingenemyspeed = attemptedspeed
    print str(flyingenemyspeed) + ' flyingenemy speed on respawn'


def reusecactus():
    cactusenemy.rect.x = 1900
    cactusenemy.rect.y = 525
    endtime = time.time()
    global cactusspeed
    attemptedspeed = (random.randint(-8, -1))-(int(endtime-starttime))/6
    if int(attemptedspeed) > -5:
        cactusspeed = random.randint(-8, -6)
    else:
        cactusspeed = attemptedspeed
    print str(cactusspeed) + ' cactus speed speed on respawn'

while mainloop == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #if a key is pressed
            print('key pressed')

            if event.key == pygame.K_DOWN:
                print('down')
                player.duck()   
                if collide == False:
                    collisioncheck(player, enemy)
                    collisioncheck(player, flyingenemy)
                    collisioncheck(player, cactusenemy)

            if event.key == pygame.K_UP:
                print('up')
                a = 1
                while a < 23 and collide == False:
                    player.jump(-a)
                    enemy.control(enemyspeed, 0)
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

                a = 1
                while a < 23 and collide == False:
                    player.jump(a)
                    enemy.control(enemyspeed, 0)
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
                    #print 'in loop'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.unduck()
                if collide == False:
                    collisioncheck(player, enemy)
                    collisioncheck(player, flyingenemy)
                    collisioncheck(player, cactusenemy)

            if event.key == pygame.K_UP:
                player.stop()
                enemy.stop()
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

    if(enemy.rect.x < 0):
        reuseenemy()
    
    if(cactusenemy.rect.x < 0):
        reusecactus()

    #global flyingenemyspawned
    if(flyingenemyspawned == False):
        print 'random flying enemy spawned'
        global flyingenemyspawned
        flyingenemyspawned = True

    elif((flyingenemy.rect.x < 0) and ((timediffint % 8) == 0)):
        print ' trying to spawn random flying enemy'
        if(((random.randint(2,10)) % 2) == 0):
            print  ' random flying enemy REUSED '
            reuseflyingenemy()
    
    #clock.tick(fps)

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
