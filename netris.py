__author__ = 'Eric'


import pygame, sys
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption('Netris v.0.1')

while True: # main game loop
    for event in pygame.event.get(): # event handler


        if event.type == QUIT: # exits the game safely
            pygame.quit()
            sys.exit()
    pygame.display.update()