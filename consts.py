__author__ = 'Eric'

import pygame
from pygame.locals import USEREVENT
from classes import *

# Initializers
pygame.init()
disp = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Netris v.0.1')

# screen constants
SCREEN_W = pygame.display.Info().current_w
SCREEN_H = pygame.display.Info().current_h
BOX_SIZE = SCREEN_H/30

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (50, 50, 50)
LIGHT_GREY = (180, 180, 180)

# shape constants/coordinates (for the sprite sheet)
BLOCK_FILE = "assets/block_sheet.png"
SHADOW_FILE = "assets/block_shadows.png"
BLOCKS = { 'I' : (('E','E','E','E'),
                  ('I','I','I','I'),
                  ('E','E','E','E'),
                  ('E','E','E','E')),

           'J' : (('J','E','E'),
                  ('J','J','J'),
                  ('E','E','E')),

           'L' : (('E','E','L'),
                  ('L','L','L'),
                  ('E','E','E')),

           'O' : (('E','O','O','E'),
                  ('E','O','O','E'),
                  ('E','E','E','E')),

           'S' : (('E','S','S'),
                  ('S','S','E'),
                  ('E','E','E')),

           'T' : (('E','T','E'),
                  ('T','T','T'),
                  ('E','E','E')),

           'Z' : (('Z','Z','E'),
                  ('E','Z','Z'),
                  ('E','E','E'))}
SPRITE_COORD =  { 'I' : (0,0,24,24),
                  'J' : (24,0,24,24),
                  'L' : (48,0,24,24),
                  'O' : (72,0,24,24),
                  'S' : (96,0,24,24),
                  'T' : (120,0,24,24),
                  'Z' : (144,0,24,24)}

# event ids
INPUT_TIMER = USEREVENT
DROP_TIMER = USEREVENT+1

# Fonts
scoreFont = pygame.font.SysFont("monospace",24)
menuFont = font = pygame.font.Font("assets/spacerangeracad.ttf",BOX_SIZE*2)

# Sprite array
sheet = pygame.image.load(BLOCK_FILE).convert()
sprites = {'I' : Block(sheet,'I'),
          'J' : Block(sheet,'J'),
          'L' : Block(sheet,'L'),
          'O' : Block(sheet,'O'),
          'S' : Block(sheet,'S'),
          'T' : Block(sheet,'T'),
          'Z' : Block(sheet,'Z')}
shadowsheet = pygame.image.load(SHADOW_FILE).convert()
shadowsprites = {'I' : Block(shadowsheet,'I'),
          'J' : Block(shadowsheet,'J'),
          'L' : Block(shadowsheet,'L'),
          'O' : Block(shadowsheet,'O'),
          'S' : Block(shadowsheet,'S'),
          'T' : Block(shadowsheet,'T'),
          'Z' : Block(shadowsheet,'Z')}