################################################################################
#
#  Contains the Cell class.  These are the building blocks for grids, whether
#  they are used for the playing board, or other piece-displaying grids.
#
################################################################################

__author__ = 'Eric'

import pygame
from modules.consts import *

# Class representing a single cell of a grid
# surface: surface upon which the contents of the cell may be drawn
# contents: represent what the cell contains
# hidden: true if this cell shouldn't be rendered
class Cell(object):
    # Constructor
    def __init__(self, hidden = False):
        x = BOX_SIZE-1
        self.surface = pygame.Surface((BOX_SIZE,BOX_SIZE))
        self.contents = 'E'
        self.hidden = hidden
        if not hidden:
            pygame.draw.line(self.surface, GREY, (0,0), (0,x), 1)
            pygame.draw.line(self.surface, GREY, (x,0), (x,x), 1)
            pygame.draw.line(self.surface, GREY, (0,0), (x,0), 1)
            pygame.draw.line(self.surface, GREY, (0,x), (x,x), 1)
