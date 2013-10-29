__author__ = 'Eric'

from pygame.locals import USEREVENT

# screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_WIDTH = 240
BOARD_HEIGHT = 480
NEXT_BOX_SIZE = 96

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

# shape constants/coordinates (for the sprite sheet)
BLOCK_FILE = "assets/block_sheet.png"
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
SPRITE_COORD =  { 'I' : (0,0,23,23),
                  'J' : (24,0,23,23),
                  'L' : (48,0,23,23),
                  'O' : (72,0,23,23),
                  'S' : (96,0,23,23),
                  'T' : (120,0,23,23),
                  'Z' : (144,0,23,23)}

# event ids
INPUT_TIMER = USEREVENT
DROP_TIMER = USEREVENT+1