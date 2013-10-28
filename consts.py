__author__ = 'Eric'

from pygame.locals import USEREVENT

# screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_WIDTH = 240
BOARD_HEIGHT = 480
BLOCK_SIZE = 24
NEXT_BOX_SIZE = 120

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (192, 192, 192)

# shape constants/coordinates (for the sprite sheet)
BLOCK_FILE = "assets/tetromino_sheet.png"
I_BLOCK = ((0, 0, 95, 23), (0, 50, 23, 95))
J_BLOCK = ((101, 0, 71, 47), (125, 50, 47, 71), (100, 124, 71, 47), (124, 174, 47, 71))
L_BLOCK = ((178, 0, 71, 47), (178, 50, 47, 71), (178, 124, 71, 47), (178, 174, 47, 71))
O_BLOCK = ((254, 0, 47, 47),)
S_BLOCK = ((306, 0, 71, 47), (306, 50, 47, 71))
T_BLOCK = ((382, 0, 71, 47), (382, 50, 47, 71), (382, 124, 71, 47), (382, 174, 47, 71))
Z_BLOCK = ((458, 0, 71, 47), (482, 50, 47, 71))
BLOCKS = (I_BLOCK, J_BLOCK, L_BLOCK, O_BLOCK, S_BLOCK, T_BLOCK, Z_BLOCK)

# event ids
INPUT_TIMER = USEREVENT+1