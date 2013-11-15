################################################################################
#
#  Contains various constants for use by other modules
#
################################################################################

__author__ = 'Eric'

import pygame
from pygame.locals import USEREVENT

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

# event ids
INPUT_TIMER = USEREVENT+1
DROP_TIMER = USEREVENT+2

# Fonts
scoreFont = pygame.font.SysFont("monospace",24)
menuFont = font = pygame.font.Font("assets/spacerangeracad.ttf",BOX_SIZE*3)