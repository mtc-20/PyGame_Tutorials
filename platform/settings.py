#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:22:52 2019

@author: mtc-20
"""

TITLE = "My Platformer!"
WIDTH = 480
HEIGHT = 600
FPS = 60
HS_FILE = "hiscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

FONT_NAME = 'purisa' # game font
STD_FONT = 'arial'



# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0,155,155)
PALEGREEN = (50, 255, 50)
MARIO_BLUE = (51, 153, 255)



# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game properties
BGCOLOR = LIGHTBLUE
BOOST_POWER = 60
PU_SPAWN_RATE = 5
MOB_FREQ = 5000

PLAYER_LAYER = 2
MOB_LAYER = 2
PLATFORM_LAYER = 1
PUP_LAYER = 1
CLOUD_LAYER = 0

# Starting platforms
#PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40), (WIDTH/2 - 50, HEIGHT*3/4, 100, 20), (125, HEIGHT-350, 100, 20), (350, 200, 100, 10), (175, 100, 100, 10)]
PLATFORM_LIST = [(0, HEIGHT - 60), (WIDTH/2 - 50, HEIGHT*3/4), (125, HEIGHT-350), (350, 200), (175, 100)]