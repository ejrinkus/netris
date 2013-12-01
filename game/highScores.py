__author__ = 'Eric'

import pygame
import eztext
from pygame.locals import *
from game.consts import *

class HighScores:

    def main(self):
        disp.fill(BLACK)
        for i in range(1,11):
            entry = " ".join(GAME_DATA["Score " + str(i)])
            scoreLabel = menuFont.render(entry, False, LIGHT_GREY)
            disp.blit(scoreLabel, (SCREEN_W/2 - scoreLabel.get_width()/2, i*BOX_SIZE*2.5))
        pygame.display.update()

        # Input loop
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    disp.fill(BLACK)
                    return
