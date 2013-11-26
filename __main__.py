################################################################################
#
#  Main module.  Starts the game and opens to main menu for naviagation.
#
################################################################################

__author__ = 'Eric'

import sys
import pickle
import pygame
from pygame.locals import *
from game.consts import *
from game.single import SinglePlayerGame
from game.options import OptionsMenu

# Set up the fonts and logo for the menu
singleLabel = menuFont.render("Single Player", False, LIGHT_GREY)
singleRect = pygame.Rect((SCREEN_W/2 - singleLabel.get_width()/2, SCREEN_H/2 - BOX_SIZE*3),
                              (singleLabel.get_width(), singleLabel.get_height()))
multiLabel = menuFont.render("Multiplayer", False, LIGHT_GREY)
multiRect = pygame.Rect((SCREEN_W/2 - multiLabel.get_width()/2, SCREEN_H/2),
                              (multiLabel.get_width(), multiLabel.get_height()))
optionsLabel = menuFont.render("Options", False, LIGHT_GREY)
optionsRect = pygame.Rect((SCREEN_W/2 - optionsLabel.get_width()/2, SCREEN_H/2 + BOX_SIZE*3),
                              (optionsLabel.get_width(), optionsLabel.get_height()))
quitLabel = menuFont.render("Quit Game", False, LIGHT_GREY)
quitRect = pygame.Rect((SCREEN_W/2 - quitLabel.get_width()/2, SCREEN_H/2 + BOX_SIZE*6),
                              (quitLabel.get_width(), quitLabel.get_height()))

# Options Screen
OPTIONS_MENU = OptionsMenu()

# Render loop
while True:
    # Draw Logo
    disp.blit(LOGO, (SCREEN_W/2 - LOGO.get_width()/2, BOX_SIZE*2))

    # Draw Text
    disp.blit(singleLabel, (singleRect.left, singleRect.top))
    disp.blit(multiLabel, (multiRect.left, multiRect.top))
    disp.blit(optionsLabel, (optionsRect.left, optionsRect.top))
    disp.blit(quitLabel, (quitRect.left, quitRect.top))
    pygame.display.update()

    # Input Loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            # Clicked Single Player
            if singleRect.collidepoint(event.pos):
                game = SinglePlayerGame()
                game.main()
                disp.fill(BLACK)

            # Clicked Multiplayer
            if multiRect.collidepoint(event.pos):
                print "Multiplayer"

            # Clicked Options
            if optionsRect.collidepoint(event.pos):
                OPTIONS_MENU.main()

            # Clicked Quit Game
            if quitRect.collidepoint(event.pos):
                pickle.dump(GAME_DATA, open("gd.dat",'wb'), -1)
                pygame.quit()
                sys.exit()


