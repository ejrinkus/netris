################################################################################
#
#  Contains the Pause class.  This class is responsible for displaying and
#  removing the pause screen overlay during a game (will not be needed in modes
#  with more than one human player, since pausing won't be allowed).
#
################################################################################
__author__ = 'Eric'

import pygame
from consts import *

# Class containing information for drawing the pause screen overlay
# self.game: reference to the game currently being played
# self.next_cover: covers the next piece box
# self.hold_cover: covers the hold piece box
# self.board_cover: covers the playing board
class GameOver(object):

    # Constructor
    # game: reference to the game being played
    def __init__(self, game):
        self.game = game
        self.next_cover = pygame.Surface((BOX_SIZE*5, BOX_SIZE*5))
        self.next_cover.fill(BLACK)
        self.hold_cover = pygame.Surface((BOX_SIZE*5, BOX_SIZE*5))
        self.hold_cover.fill(BLACK)
        self.board_cover = pygame.Surface((BOX_SIZE*10-9, BOX_SIZE*20))
        self.board_cover.fill(BLACK)
        game_label = pauseFont.render("Game", False, LIGHT_GREY)
        self.board_cover.blit(game_label,
                              (BOX_SIZE*5-game_label.get_width()/2, BOX_SIZE*10-game_label.get_height()/2))
        over_label = pauseFont.render("Over", False, LIGHT_GREY)
        self.board_cover.blit(over_label,
                              (BOX_SIZE*5-over_label.get_width()/2, BOX_SIZE*10-game_label.get_height()/2+over_label.get_height()))

    # Displays the pause overlay (which should hide the board, next piece box, and hold piece box)
    def gameover(self):
        disp.blit(self.board_cover, (self.game.board.location[0], self.game.board.location[1]+BOX_SIZE*2-2))
        disp.blit(self.hold_cover, (self.game.hold_box.location[0], self.game.hold_box.location[1]))
        disp.blit(self.next_cover, (self.game.next_box.location[0], self.game.next_box.location[1]))
        score = self.game.score
        name = GAME_DATA["User Name"][0]
        for i in range(1,11):
            if int(GAME_DATA["Score "+str(i)][1]) < score:
                temp_score = score
                score = int(GAME_DATA["Score "+str(i)][1])
                GAME_DATA["Score "+str(i)][1] = str(temp_score)
                temp_name = name
                name = GAME_DATA["Score "+str(i)][0]
                GAME_DATA["Score "+str(i)][0] = temp_name
