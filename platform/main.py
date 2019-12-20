#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:25:01 2019

@author: mtc-20

TODO: Save name along with hi-score
TODO: Improve platform generation: within jumpable distance? ; avoid overlapping?
TODO: More powerups and enemies: (shooting)
"""

import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        self.running = True
        # initialize pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        
    def load_data(self):
        # load spritesheet
        self.dir = path.dirname(__file__)
        image_dir = path.join(self.dir, 'Spritesheets')
        self.spritesheet = Spritesheet(path.join(image_dir, SPRITESHEET))
        
        # load cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(image_dir, 'cloud{}.png'.format(i))).convert())
        # load scorelog
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.hiscore = int(f.read())
            except Exception as e:
                self.hiscore = 0
                print(e, type(e))
                
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav'))
        self.boost_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup5.wav'))
        self.coin_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Pickup_Coin4.wav'))
        
        
    def new(self):
        # start new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.pups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
#        self.all_sprites.add(self.player)
        for pos in PLATFORM_LIST:
            Platform(*pos, self)
#            p = Platform(*pos, self)
#            self.all_sprites.add(p)
#            self.platforms.add(p)
        
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        pg.mixer.music.set_volume(0.6)
        self.mob_timer = 0
            
#        self.platform = Platform(0,HEIGHT-40, WIDTH, 40)
#        self.all_sprites.add(self.platform)
#        self.platforms.add(self.platform)
#        self.p2 = Platform(WIDTH/2, HEIGHT/2+40, 80, 20)
#        self.all_sprites.add(self.p2)
#        self.platforms.add(self.p2)
        self.run()
        
    def run(self):
        # game loop
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
        
    def events(self):
        # game loop update
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check for jump command
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            # check for jump power
            if event.type == pg.KEYUP:  
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                
                if event.key == pg.K_ESCAPE:
                    self.show_pause_screen()
                
    def update(self):
        self.all_sprites.update()
        
        # Spawn mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # Check for platform collision
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            lowest = hits[0]
            for hit in hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest
            if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
                    
        # Check for mob collision
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if hits:
            self.playing = False
            
        # Activate Powerups
        pow_hits = pg.sprite.spritecollide(self.player, self.pups, True)
        for po in pow_hits:
            if po.type == 'boost':
                self.boost_snd.play()
                self.player.vel.y = - BOOST_POWER
                self.player.jumping = False
            
            elif po.type == 'coin':
                self.coin_snd.play()
                self.score += 100
        
        # Scrolling effect
        if self.player.rect.top <= HEIGHT/4:
            if random.randrange(100) < 5:
                Cloud(self)
                
            self.player.pos.y += max(abs(self.player.vel.y),3)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y/randrange(2,4)), 3)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 3)
                if mob.rect.top > HEIGHT:
                    self.score += 5
            for plat in self.platforms:
               plat.rect.y += max(abs(self.player.vel.y),3)
               if plat.rect.top > HEIGHT:
                   if plat.rect.width > 100:
                       scaler = 10
                   else:
                       scaler = 100 - plat.rect.width
                   plat.kill()
                   self.score += scaler
        # spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50,100)
            Platform(random.randrange(0, WIDTH - width), random.randrange(-75, -30), self)
#            p = Platform(random.randrange(0, WIDTH - width), random.randrange(-75, -30), self)
#            self.all_sprites.add(p)
#            self.platforms.add(p)
            
        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                if len(self.platforms) == 0:
                    self.playing = False
                    self.player.kill()
#                    pg.quit()
                
        
        
    def draw(self):
        self.screen.fill(BGCOLOR)
#        screen.blit(background, background_rect)
        self.all_sprites.draw(self.screen)
        
#        # ensure player is upfront
#        self.screen.blit(self.player.image, self.player.rect)
        
        self.draw_text(str(self.score),22, WHITE, WIDTH/2, 10, STD_FONT)
        # *after* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        pg.mixer.music.set_volume(0.5 )
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, SPACE to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("HI SCORE: " + str(self.hiscore), 22, WHITE, WIDTH/2, 10, 'chilanka')
        self.draw_text("Press any key to start...", 20, WHITE, WIDTH/2, HEIGHT*3/4, STD_FONT)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        
    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 42, RED, WIDTH/2, HEIGHT/4, 'chilanka')
        self.draw_text("Your score: " + str(self.score), 36, WHITE, WIDTH/2, HEIGHT/2, 'chilanka')
        self.draw_text("Press any key to restart...", 20, WHITE, WIDTH/2, HEIGHT*3/4, STD_FONT)
        if self.score > self.hiscore:
            self.draw_text("NEW HI SCORE!", 22, WHITE, WIDTH/2, HEIGHT/2 + 40, 'chilanka')
            with open(path.join(self.dir,HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("HI SCORE: " + str(self.hiscore), 22, WHITE, WIDTH/2, HEIGHT/2 + 40, 'chilanka')
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        
    def show_pause_screen(self):
        #self.screen.fill(BGCOLOR)
        self.draw_text("Game Paused", 36, WHITE, WIDTH/2, HEIGHT/4 - 50)
        self.draw_text("Press any key to continue...", 20, WHITE, WIDTH/2, HEIGHT*3/4, STD_FONT)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    self.playing = False
                if event.type == pg.KEYUP:
                    waiting = False
            self.clock.tick(FPS)
            
    
    def draw_text(self, text, size, color, x, y, font_name= None):
        if font_name==None:
            font_name = self.font_name
        else:
            font_name = pg.font.match_font(font_name)
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.show_go_screen()
pg.quit()