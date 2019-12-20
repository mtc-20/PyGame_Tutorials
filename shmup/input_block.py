#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 10:26:10 2019

@author: comp1
"""

import pygame
from pygame.locals import *
from datetime import datetime

FPS = 60
clock = pygame.time.Clock()
def name(value):
    pygame.init()
    screen = pygame.display.set_mode((480, 360))
    background = pygame.image.load('img/starfield.png').convert()
    background_rect = background.get_rect()
    now = datetime.now()
    qn = "Please enter name"
    name = ""
    font = pygame.font.Font(None, 50)
    completion = True
    while completion:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
#                    name = ""
                    f = open("score_{}.txt".format(now.strftime("%m%d%Y")), "a")
                    f.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " : " + name + " : {}".format( value) + "\n")
                    completion = False
                    f.close()
            elif evt.type == QUIT:
                return
        screen.fill((0, 0, 0))
        name_block = font.render(name, True, (255, 255, 255))
        name_rect = name_block.get_rect()
        name_rect.center = screen.get_rect().center
        qn_block = font.render(qn, True, (100, 0, 255))
        qn_rect = qn_block.get_rect()
        qn_rect.x = 20
        qn_rect.y = 5
        
        screen.blit(background, background_rect)
        screen.blit(name_block, name_rect)
        screen.blit(qn_block, qn_rect)
        pygame.display.flip()
        
def display_scorelist():
    WIDTH = 6000
    HEIGHT = 600
    x = 10
    y = 5
    pygame.init()
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
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

if __name__ == "__main__":
    name(100)
    display_scorelist()
    pygame.quit()