#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 13:14:45 2019

@author: mtc-20
"""

# Pygame template - skeleton for a new pygame project
import pygame
import random
from input_block import name
from datetime import datetime

# Base Settings
WIDTH = 480
HEIGHT = 600
FPS = 60
SCORE = 0
POWERUP_TIME = 3000
LEVEL = 2500

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0,100,100)
ORANGE = (255, 165, 0)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Space Shooter")
clock = pygame.time.Clock()

# Load game graphics
background = pygame.image.load('img/starfield.png').convert()
background_rect = background.get_rect()

player_img = pygame.image.load('img/playerShip1_orange.png').convert()
laser_img = pygame.image.load('img/laserRed16.png').convert()

mob_img = pygame.image.load('img/meteorBrown_med1.png').convert()
meteor_images = []
meteor_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load("img/{}".format(img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (30,30))
    explosion_anim['sm'].append(img_sm)
    filename = 'img/sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

pow_images = {}
pow_images["shield"] = pygame.image.load("img/shield_gold.png").convert()
pow_images["gun"] = pygame.image.load("img/bolt_gold.png").convert()


# Load game sounds
shoot_sound = pygame.mixer.Sound('snd/pew.wav')
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound('snd/{}'.format(snd)))
    
pygame.mixer.music.load('snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
pygame.mixer.music.set_volume(1)

# Sprite Deifnitions
# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
#        self.image = pygame.Surface((50, 40))
#        self.image.fill(GREEN)
        self.shield = 100
#        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()	
        self.radius = 25
#        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        # Extra Lives
        self.lives = 1
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # Power up
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            
        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.hidden and pygame.time.get_ticks() - self.hide_timer >1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
            
        # powerup timeout
        if self.power>=2  and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Laser(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                lasers.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Laser(self.rect.left, self.rect.centery)
                bullet2 = Laser(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                lasers.add(bullet1)
                lasers.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Laser(self.rect.left, self.rect.centery)
                bullet2 = Laser(self.rect.right, self.rect.centery)
                bullet3 = Laser(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                lasers.add(bullet1)
                lasers.add(bullet2)
                lasers.add(bullet3)
                shoot_sound.play()
            
            
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)
        
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
#        self.image = pygame.Surface((30,40))
        self.image_orig = random.choice(meteor_images)
#        self.image_orig = mob_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
#        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.9/2)
#        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        
#        if self.rect.right > WIDTH:
#            self.rect.right = WIDTH
#            
#        if self.rect.left < 0:
#            self.rect.left = 0
            
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 75:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            

class Laser(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
#        self.image = pygame.Surface((10,20))
        self.image = laser_img
#        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
        
    def update(self):
        self.rect.y += self.speedy  
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image =  explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            
        else:
            center = self.rect.center
            self.image = explosion_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            
            

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield","gun"])
        self.image = pow_images[self.type]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
        
                    

#
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def newmob(lvl=0):
    m = Mob()
    if lvl == 2:
        m.speedy = random.randrange(10,16)
        m.speedx = random.randrange(-5,5)
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    BAR_COLOR = GREEN
    if pct/100 < 0.2:
        BAR_COLOR = RED
    elif pct/100 < 0.6:
        BAR_COLOR = ORANGE
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BAR_COLOR, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)
        
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Arrows to move, SPACE to fire", 22, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
def display_scorelist():
#    WIDTH = 600
    HEIGHT = 800
    x = 10
    y = 5
#    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    now = datetime.now()
    font = pygame.font.Font(None, 20)
    background = pygame.image.load('img/starfield.png').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    title_block = font.render("DAILY SCORES", True, (255, 255, 255))
    title_rect = title_block.get_rect()
    title_rect.x = x
    title_rect.y = y
    screen.blit(title_block, title_rect)
    waiting = True
    with open("score_{}.txt".format(now.strftime("%m%d%Y"))) as fp:
        line = fp.readline()
        cnt = 1
        while line or cnt < 25 :
#            print(" {} {}".format(cnt, line.strip()))
            y += 25
            block = font.render(" {} {}".format(cnt, line.strip()), True, (255, 255, 255))
            block_rect = block.get_rect()
            block_rect.x = x
            block_rect.y = y
            screen.blit(block, block_rect)
            line = fp.readline()
            cnt += 1
    fp.close()
    pygame.display.flip()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP: 
                waiting = False
                pygame.quit()
        clock.tick(FPS)
                
#            if event.type == pygame.KEYUP:
#                waiting = False


#''' 
#Initialise sprites and groups
#'''
#all_sprites = pygame.sprite.Group()
#player = Player()
#all_sprites.add(player)
#
#mobs = pygame.sprite.Group()
#for i in range(8):
#    newmob()
#
#lasers = pygame.sprite.Group()
#pow_ups = pygame.sprite.Group()

''' 
Game loop
'''
running = True
game_over = True
pygame.mixer.music.play(loops=-1)
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        lasers = pygame.sprite.Group()
        pow_ups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            newmob()
        SCORE = 0

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        
    # Update
    all_sprites.update()
    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
#            player.kill()
#            running = False
            player.hide()
            player.shield = 100
            player.lives -= 1
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, lasers, True, True)
    for strike in hits:
        SCORE += 50 - strike.radius
        random.choice(expl_sounds).play()
        expl = Explosion(strike.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow_up = Pow(strike.rect.center)
            all_sprites.add(pow_up)
            pow_ups.add(pow_up)
        newmob()
        
    hits = pygame.sprite.spritecollide(player, pow_ups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += random.randint(10,30)
            if player.shield > 100:
                player.shield = 100
        if hit.type == "gun":
            player.powerup()
            
    if SCORE > LEVEL:
        for i in range(4):
            newmob(2)
        LEVEL += LEVEL/2
        
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(SCORE), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
#    draw_text(screen, 'Shield: {}'.format(player.shield), 18, 0, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()
    if player.lives <= 0 and not death_expl.alive():
        running = False
#        game_over = True
    # keep loop running at the right speed
    clock.tick(FPS)

name(SCORE)    
print("Score: %i" %SCORE)
display_scorelist()    
#pygame.quit()