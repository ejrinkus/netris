################################################################################
#
#  Main module.  Starts the game and opens to main menu for naviagation.
#
################################################################################

__author__ = 'Eric'

# All the fun little imports
import sys
import pygame
from pygame.locals import *
from modules.consts import *
from modules.gametypes.single import SinglePlayerGame

# Set up the fonts and logo for the menu
singleLabel = menuFont.render("Single Player", False, LIGHT_GREY)
multiLabel = menuFont.render("Multiplayer", False, LIGHT_GREY)
optionsLabel = menuFont.render("Options", False, LIGHT_GREY)
quitLabel = menuFont.render("Quit Game", False, LIGHT_GREY)
logo = pygame.image.load("assets/logo.png").convert()

# Render loop
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
            # Clicked Single Player
            if SCREEN_W/2 - singleLabel.get_width()/2 <= event.pos[0] <= SCREEN_W/2 + singleLabel.get_width()/2 and \
                            SCREEN_H/2 - BOX_SIZE*2 <= event.pos[1] <= SCREEN_H/2:
                game = SinglePlayerGame()
                game.main()
                disp.fill(BLACK)

            # Clicked Multiplayer
            if SCREEN_W/2 - multiLabel.get_width()/2 <= event.pos[0] <= SCREEN_W/2 + multiLabel.get_width()/2 and \
                            SCREEN_H/2 <= event.pos[1] <= SCREEN_H/2 + BOX_SIZE*2:
                print "Multiplayer"

            # Clicked Options
            if SCREEN_W/2 - optionsLabel.get_width()/2 <= event.pos[0] <= SCREEN_W/2 + optionsLabel.get_width()/2 and \
                            SCREEN_H/2 + BOX_SIZE*2 <= event.pos[1] <= SCREEN_H/2 + BOX_SIZE*4:
                print "Options"

            # Clicked Quit Game
            if SCREEN_W/2 - quitLabel.get_width()/2 <= event.pos[0] <= SCREEN_W/2 + quitLabel.get_width()/2 and \
                            SCREEN_H/2 + BOX_SIZE*4 <= event.pos[1] <= SCREEN_H/2 + BOX_SIZE*6:
                pygame.quit()
                sys.exit()
