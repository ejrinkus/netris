################################################################################
#
#  Contains the SinglePlayerGame class.  This class has the main render and
#  logic loop for playing a single player game.
#
################################################################################
from game.Grid import Grid
from game.Tetromino import Tetromino

__author__ = 'Eric'

import sys
from random import shuffle

import pygame
from pygame.locals import *

from game.consts import *
from game.pause import Pause


class SinglePlayerGame(object):

    # Constructor
    def __init__(self):
        disp.fill(BLACK)

        # Flags and other necessary variables
        self.paused = False
        self.spawn = True
        self.hold = False
        self.hold_flag = False
        self.first_hold = False
        pygame.time.set_timer(INPUT_TIMER, 50)
        pygame.time.set_timer(DROP_TIMER, 1000)
        self.u_hold = self.d_hold = self.l_hold = self.r_hold = 3
        self.up = self.down = self.left = self.right = False
        self.u_first = self.d_first = self.l_first = self.r_first = False
        self.order = ['I','J','L','O','S','T','Z']
        shuffle(self.order)
        self.count = 0
        self.nextpiece = Tetromino(self.order[self.count])
        self.heldpiece = Tetromino()
        self.activepiece = Tetromino()
        self.cleared = 0
        self.timeFlag = False
        self.speed = 1000.0
        self.score = 0
        self.level = 1
        self.shadowPiece = None
        self.lock = False
        self.pause = Pause(self)

        # Playing board
        self.board = Grid((SCREEN_W/2 - BOX_SIZE*5, BOX_SIZE/5), 10, 22, (0,1))
        self.board.drawChanges(disp)

        # Next piece box
        self.next_box = Grid((self.board.location[0] - BOX_SIZE*7, BOX_SIZE/5 + BOX_SIZE*2), 5, 5)
        self.next_box.drawChanges(disp)

        # Hold box
        self.hold_box = Grid((self.board.location[0] + BOX_SIZE*12, BOX_SIZE/5 + BOX_SIZE*2), 5, 5)
        self.hold_box.drawChanges(disp)

    # Clears the given piece from the board
    def clearPiece(self,p):
        if p is None: return
        for i, row in enumerate(p.matrix):
            for j, block in enumerate(row):
                if block != 'E':
                    self.board.clearCell(i+p.coord[1], j+p.coord[0])
        self.board.clearShadow(p);

    # Main function for playing single player
    def main(self):
        # Main game loop
        while True:

            # Set speed appropriate to level
            if self.timeFlag:
                self.timeFlag = False
                self.speed *= 0.8944272
                self.level += 1
                pygame.time.set_timer(DROP_TIMER, int(self.speed))

            # Switch out the held piece
            if self.hold:
                self.hold = self.hold_flag = False
                self.clearPiece(self.activepiece)
                temp = self.activepiece.id
                self.activepiece = Tetromino(self.heldpiece.id)
                self.heldpiece = Tetromino(temp)
                self.heldpiece.coord = [1,1]
                # Draw held piece
                self.hold_box.clear()
                self.hold_box.drawPiece(self.heldpiece)
                # Prepare active piece for drawing (or spawn new piece if there was no held piece)
                if self.activepiece.id == 'E':
                    self.spawn = True
                    self.first_hold = True

            # Spawn a new piece, and determine the next piece
            if self.spawn:
                self.spawn = False
                if self.first_hold: self.first_hold = False
                else: self.hold_flag = True
                self.activepiece = Tetromino(self.nextpiece.id)
                self.count += 1
                if self.count > 6:
                    self.count = 0
                    shuffle(self.order)
                self.nextpiece = Tetromino(self.order[self.count])
                self.nextpiece.coord = [1,1]
                self.next_box.clear()
                # Draw next piece
                self.next_box.drawPiece(self.nextpiece)
                if not self.board.validPos(self.activepiece): return
            else:
                self.clearPiece(self.activepiece)

            # Event handler
            for event in pygame.event.get():
                # Register a key being pressed
                if event.type == KEYDOWN:
                    if not self.paused:
                        if event.key == K_UP:
                            self.clearPiece(self.activepiece)
                            while self.board.validMoveDown(self.activepiece): continue
                            self.lock = True
                        if event.key == K_LEFT:
                            self.left = self.l_first = True
                            self.l_hold = 3
                        if event.key == K_RIGHT:
                            self.right = self.r_first = True
                            self.r_hold = 3
                        if event.key == K_DOWN:
                            self.down = self.d_first = True
                            self.d_hold = 3
                        if event.key == K_LCTRL and self.activepiece.id != 'O':
                            self.clearPiece(self.activepiece)
                            self.board.validRotLeft(self.activepiece)
                        if event.key == K_RCTRL and self.activepiece.id != 'O':
                            self.clearPiece(self.activepiece)
                            self.board.validRotRight(self.activepiece)
                        if event.key == K_SPACE and self.hold_flag:
                            self.hold = True

                    # Pause/exit the game
                    if event.key == K_p:
                        self.left = self.l_first = False
                        self.right = self.r_first = False
                        self.down = self.d_first = False
                        self.paused = True
                        self.pause.pause()

                    if event.key == K_ESCAPE:
                        return

                # Key was released
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.left = self.l_first = False
                    if event.key == K_RIGHT:
                        self.right = self.r_first = False
                    if event.key == K_DOWN:
                        self.down = self.d_first = False

                # Exits the game safely
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Move the piece (timer used to control the hold speed)
                if event.type == INPUT_TIMER:
                    if not self.paused:
                        self.clearPiece(self.activepiece)
                        if self.left:
                            if self.l_first or self.l_hold <= 0:
                                self.board.validMoveLeft(self.activepiece)
                                self.l_first = False
                            else: self.l_hold -= 1
                        if self.right:
                            if self.r_first or self.r_hold <= 0:
                                self.board.validMoveRight(self.activepiece)
                                self.r_first = False
                            else: self.r_hold -= 1
                        if self.down:
                            if self.d_first or self.d_hold <= 0:
                                if not self.board.validMoveDown(self.activepiece): self.lock = True
                                self.d_first = False
                            else: self.d_hold -= 1

                # Drop the piece one step
                if event.type == DROP_TIMER:
                    if not self.paused:
                        self.clearPiece(self.activepiece)
                        if not self.board.validMoveDown(self.activepiece):
                            self.spawn = True
                            self.lock = True

            while self.paused:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_p:
                        self.paused = False
                        self.pause.unpause()
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        return
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()


            # Draw the piece and shadow to the board
            self.board.drawPiece(self.activepiece,self.lock)
            self.lock = False
            self.board.drawShadow(self.activepiece)

            # Check rows for clearing
            if self.spawn:
                temp = 0
                for i in xrange(self.board.height):
                    if self.board.clearRow(i):
                        self.cleared += 1
                        temp += 1
                        if self.cleared % 5 == 0: self.timeFlag = True
                if temp == 1:
                    self.score += 100*self.level
                elif temp == 2:
                    self.score += 300*self.level
                elif temp == 3:
                    self.score += 500*self.level
                elif temp == 4:
                    self.score += 800*self.level

            # Draw everything to the screen
            self.next_box.drawChanges(disp)
            self.hold_box.drawChanges(disp)
            self.board.drawChanges(disp)
            levellabel = scoreFont.render("Level: "+str(self.level), 1, LIGHT_GREY)
            scorelabel = scoreFont.render("Score: "+str(self.score), 1, LIGHT_GREY)
            nextlabel = scoreFont.render("Next Piece", 1, LIGHT_GREY)
            holdlabel = scoreFont.render("Held Piece", 1, LIGHT_GREY)
            disp.blit(pygame.Surface((SCREEN_W, BOX_SIZE*2)), (0,0))
            disp.blit(levellabel, (SCREEN_W/2 - BOX_SIZE*5, 0))
            disp.blit(scorelabel, (SCREEN_W/2 - BOX_SIZE*5, BOX_SIZE))
            disp.blit(nextlabel, (self.next_box.location[0], self.next_box.location[1] - BOX_SIZE))
            disp.blit(holdlabel, (self.hold_box.location[0], self.hold_box.location[1] - BOX_SIZE))
            pygame.display.update()
