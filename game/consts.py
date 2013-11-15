################################################################################
#
#  Contains various constants for use by other modules
#
################################################################################

__author__ = 'Eric'

import pygame, StringIO, pkgutil, os, tempfile
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
BLOCK_FILE = StringIO.StringIO(pkgutil.get_data('game', "block_sheet.png"))
SHADOW_FILE = StringIO.StringIO(pkgutil.get_data('game', "block_shadows.png"))
BLOCK_SHEET = pygame.image.load(BLOCK_FILE, "block_sheet.png").convert()
SHADOW_SHEET = pygame.image.load(SHADOW_FILE, "block_shadows.png").convert()

# event ids
INPUT_TIMER = USEREVENT+1
DROP_TIMER = USEREVENT+2

# Fonts
scoreFont = pygame.font.SysFont("monospace",24)
font_file = StringIO.StringIO(pkgutil.get_data('game', "spacerangeracad.ttf"))
menuFont = pygame.font.Font(font_file,BOX_SIZE*3)

#tmpdir = tempfile.mkdtemp()
#fname = os.path.join(tmpdir, "assets/spacerangeracad.ttf")
#try:
#    with open(fname, 'wb') as f:
#        data = pkgutil.get_data('assets', "assets/spacerangeracad.ttf")
#        f.write(data)
#    menuFont = pygame.font.Font(fname, BOX_SIZE*3)
#finally:
#    try:
#        os.remove(fname)
#        os.rmdir(tmpdir)
#    except:
#        pass