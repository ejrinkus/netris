__author__ = 'Eric'

import pygame, sys
from pygame.locals import *

# screen constants
WIDTH = 800
HEIGHT = 600
BLOCK_RECT = (0,0,23,23)

# color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
GREY = (192,192,192)

# shape constants/coordinates (for the sprite sheet)
I_BLOCK = 0
J_BLOCK = 1
L_BLOCK = 2
O_BLOCK = 3
S_BLOCK = 4
T_BLOCK = 5
Z_BLOCK = 6
BLOCKS = ((0, 0, 95, 23), (101, 0, 71, 47), (178, 0, 71, 47), (254, 0, 47, 47),
          (306, 0, 71, 47), (382, 0, 71, 47), (458, 0, 71, 47))