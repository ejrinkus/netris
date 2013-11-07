__author__ = 'Eric'

import pygame
import sys
from single import SinglePlayerGame
from pygame.locals import *
from random import shuffle
from consts import *
from classes import *

font = pygame.font.Font("assets/spacerangeracad.ttf",BOX_SIZE*2)
singleLabel = font.render("Single Player", False, LIGHT_GREY)
multiLabel = font.render("Multiplayer", False, LIGHT_GREY)
optionsLabel = font.render("Options", False, LIGHT_GREY)
quitLabel = font.render("Quit Game", False, LIGHT_GREY)
logo = pygame.image.load("assets/logo.png").convert()


while(True):
    # Draw Logo
    disp.blit(logo, (SCREEN_W/2 - logo.get_width()/2, BOX_SIZE*2))

    # Draw Text
    disp.blit(singleLabel, (SCREEN_W/2 - singleLabel.get_width()/2, SCREEN_H/2 - BOX_SIZE*2))
    disp.blit(multiLabel, (SCREEN_W/2 - multiLabel.get_width()/2, SCREEN_H/2))
    disp.blit(optionsLabel, (SCREEN_W/2 - optionsLabel.get_width()/2, SCREEN_H/2 + BOX_SIZE*2))
    disp.blit(quitLabel, (SCREEN_W/2 - quitLabel.get_width()/2, SCREEN_H/2 + BOX_SIZE*4))
    pygame.display.update();

    # Input Loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            # Start a single player game
            if SCREEN_W/2 - singleLabel.get_width()/2 <= event.pos[0] and \
                            event.pos[0] <= SCREEN_W/2 + singleLabel.get_width()/2 and \
                            SCREEN_H/2 - BOX_SIZE*2 <= event.pos[1] and \
                            event.pos[1] <= SCREEN_H/2:
                game = SinglePlayerGame()
                game.main()
                disp.fill(BLACK)

            # Exit the game
            if SCREEN_W/2 - quitLabel.get_width()/2 <= event.pos[0] and \
                            event.pos[0] <= SCREEN_W/2 + quitLabel.get_width()/2 and \
                            SCREEN_H/2 + BOX_SIZE*4 <= event.pos[1] and \
                            event.pos[1] <= SCREEN_H/2 + BOX_SIZE*6:
                pygame.quit()
                sys.exit()
