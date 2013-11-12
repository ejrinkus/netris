__author__ = 'Eric'

import pygame
import sys
from single import SinglePlayerGame
from pygame.locals import *
import consts as C
from classes import *

singleLabel = C.menuFont.render("Single Player", False, C.LIGHT_GREY)
multiLabel = C.menuFont.render("Multiplayer", False, C.LIGHT_GREY)
optionsLabel = C.menuFont.render("Options", False, C.LIGHT_GREY)
quitLabel = C.menuFont.render("Quit Game", False, C.LIGHT_GREY)
logo = pygame.image.load("assets/logo.png").convert()


while(True):
    # Draw Logo
    C.disp.blit(logo, (C.SCREEN_W/2 - logo.get_width()/2, C.BOX_SIZE*2))

    # Draw Text
    C.disp.blit(singleLabel, (C.SCREEN_W/2 - singleLabel.get_width()/2, C.SCREEN_H/2 - C.BOX_SIZE*2))
    C.disp.blit(multiLabel, (C.SCREEN_W/2 - multiLabel.get_width()/2, C.SCREEN_H/2))
    C.disp.blit(optionsLabel, (C.SCREEN_W/2 - optionsLabel.get_width()/2, C.SCREEN_H/2 + C.BOX_SIZE*2))
    C.disp.blit(quitLabel, (C.SCREEN_W/2 - quitLabel.get_width()/2, C.SCREEN_H/2 + C.BOX_SIZE*4))
    pygame.display.update();

    # Input Loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            # Start a single player game
            if C.SCREEN_W/2 - singleLabel.get_width()/2 <= event.pos[0] <= C.SCREEN_W/2 + singleLabel.get_width()/2 and \
                            C.SCREEN_H/2 - C.BOX_SIZE*2 <= event.pos[1] <= C.SCREEN_H/2:
                game = SinglePlayerGame()
                game.main()
                C.disp.fill(C.BLACK)

            # Exit the game
            if C.SCREEN_W/2 - quitLabel.get_width()/2 <= event.pos[0] <= C.SCREEN_W/2 + quitLabel.get_width()/2 and \
                            C.SCREEN_H/2 + C.BOX_SIZE*4 <= event.pos[1] <= C.SCREEN_H/2 + C.BOX_SIZE*6:
                pygame.quit()
                sys.exit()
