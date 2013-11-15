################################################################################
#
#  Contains the Block class.  Instances of this class are used to render the
#  individual blocks of a tetromino.  Allows for easy tetromino break ups during
#  line completes.
#
################################################################################

__author__ = 'Eric'

import pygame
from consts import *

# Coordinates of individual sprites within their sheet
SPRITE_COORD =  { 'I' : (0,0,24,24),
                  'J' : (24,0,24,24),
                  'L' : (48,0,24,24),
                  'O' : (72,0,24,24),
                  'S' : (96,0,24,24),
                  'T' : (120,0,24,24),
                  'Z' : (144,0,24,24)}

# Sprite sheets used by blocks
sheet = pygame.image.load(BLOCK_FILE).convert()
shadowsheet = pygame.image.load(SHADOW_FILE).convert()

# Class to display each individual block
# id: Shape the block belongs to (determines color, too)
# image: Drawable image for the block
class Block(pygame.sprite.Sprite):
    # Constructor
    # sheet: image object for the sprite sheet
    # rect_set: set of rotations for the block
    def __init__(self, t, shadow):
        super(Block, self).__init__()
        rect = pygame.Rect(SPRITE_COORD.get(t))
        self.id = t
        self.image = pygame.Surface(rect.size).convert()
        if shadow:
            self.image.blit(shadowsheet, (0, 0), rect)
        else:
            self.image.blit(sheet, (0, 0), rect)
