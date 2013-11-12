__author__ = 'Eric'

import pygame
import sys
from pygame.locals import *
from random import shuffle
import consts as C
from classes import *

class SinglePlayerGame(object):

    def __init__(self):
        C.disp.fill(C.BLACK)

        # Flags and other necessary variables
        self.paused = False
        self.spawn = True
        self.hold = False
        self.hold_flag = False
        pygame.time.set_timer(C.INPUT_TIMER, 50)
        pygame.time.set_timer(C.DROP_TIMER, 1000)
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

        # Playing board
        self.board = Grid((C.SCREEN_W/2 - C.BOX_SIZE*5, C.BOX_SIZE/5), 10, 22, (0,1))
        self.board.drawChanges(C.disp)

        # Next piece box
        self.next_box = Grid((self.board.location[0] - C.BOX_SIZE*6, C.BOX_SIZE/5 + C.BOX_SIZE*2), 5, 5)
        self.next_box.drawChanges(C.disp)

        # Hold box
        self.hold_box = Grid((self.board.location[0] + C.BOX_SIZE*11, C.BOX_SIZE/5 + C.BOX_SIZE*2), 5, 5)
        self.hold_box.drawChanges(C.disp)

    def clearPiece(self,p):
        if p is None: return
        for i, row in enumerate(p.matrix):
            for j, block in enumerate(row):
                if block != 'E':
                    if not p.shadow or (p.shadow and 0 <=  i+p.coord[1] < self.board.height and \
                                                     0 <=  j+p.coord[0] < self.board.width and \
                                                     self.board.grid[i+p.coord[1]][j+p.coord[0]].contents == 'E'):
                        self.board.clearCell(i+p.coord[1], j+p.coord[0])

    def preparePiece(self,p):
        offi = p.coord[1]
        offj = p.coord[0]
        drawCoords = []
        for i,row in enumerate(p.matrix):
            for j,block in enumerate(p.matrix[i]):
                if block != 'E':
                    if self.board.grid[i+offi][j+offj].contents == 'E': drawCoords.append((i+offi,j+offj))
                    else: return False
        for coord in drawCoords:
            self.board.changeCell(coord[0],coord[1],p)
        return True

    def makeShadow(self):
        self.shadowPiece = Tetromino(self.activepiece.id,True)
        self.shadowPiece.state = self.activepiece.state
        self.shadowPiece.matrix = self.activepiece.matrix
        self.shadowPiece.coord[0] = self.activepiece.coord[0]
        self.shadowPiece.coord[1] = self.activepiece.coord[1]

        while self.board.validMoveDown(self.shadowPiece): continue

        self.preparePiece(self.shadowPiece)

    def main(self):
        # Main game loop
        while True:

            # Set speed appropriate to level
            if self.timeFlag:
                self.timeFlag = False
                self.speed *= 0.8944272
                self.level += 1
                pygame.time.set_timer(C.DROP_TIMER, int(self.speed))

            # Switch out the held piece
            if self.hold:
                self.hold = self.hold_flag = False
                self.clearPiece(self.activepiece)
                temp = self.activepiece.id
                self.activepiece = Tetromino(self.heldpiece.id)
                self.heldpiece = Tetromino(temp)
                # Draw held piece
                self.hold_box.clear()
                for i,row in enumerate(self.heldpiece.matrix):
                    for j,block in enumerate(row):
                        if block != 'E':
                            self.hold_box.changeCell(i+1,j+1,self.heldpiece)
                        else:
                            self.hold_box.clearCell(i+1,j+1)
                # Prepare active piece for drawing (or spawn new piece if there was no held piece)
                if self.activepiece.id != 'E':
                    self.preparePiece(self.activepiece)
                else:
                    self.spawn = True

            # Spawn a new piece, and determine the next piece
            if self.spawn:
                self.spawn = False
                self.hold_flag = True
                self.activepiece = self.nextpiece
                self.count += 1
                if self.count > 6:
                    self.count = 0
                    shuffle(self.order)
                self.nextpiece = Tetromino(self.order[self.count])
                self.next_box.clear()
                # Draw next piece
                for i,row in enumerate(self.nextpiece.matrix):
                    for j,block in enumerate(row):
                        if block != 'E':
                            self.next_box.changeCell(i+1,j+1,self.nextpiece)
                        else:
                            self.next_box.clearCell(i+1,j+1)
                # Prepare active piece for drawing
                if not self.preparePiece(self.activepiece):
                    return

            # Event handler
            for event in pygame.event.get():
                # Register a key being pressed
                if event.type == KEYDOWN:
                    if not self.paused:
                        if event.key == K_UP:
                            self.clearPiece(self.activepiece)
                            while self.board.validMoveDown(self.activepiece): continue
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
                            for i, row in enumerate(self.activepiece.matrix):
                                for j, block in enumerate(row):
                                    if block != 'E':
                                        self.board.clearCell(i+self.activepiece.coord[1], j+self.activepiece.coord[0])
                            self.board.validRotLeft(self.activepiece)
                        if event.key == K_RCTRL and self.activepiece.id != 'O':
                            for i, row in enumerate(self.activepiece.matrix):
                                for j, block in enumerate(row):
                                    if block != 'E':
                                        self.board.clearCell(i+self.activepiece.coord[1], j+self.activepiece.coord[0])
                            self.board.validRotRight(self.activepiece)
                        if event.key == K_SPACE and self.hold_flag == True:
                            self.hold = True

                    # Pause/exit the game
                    if event.key == K_p:
                        self.paused = not self.paused
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
                if event.type == C.INPUT_TIMER:
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
                                self.board.validMoveDown(self.activepiece)
                                self.d_first = False
                            else: self.d_hold -= 1

                if event.type == C.DROP_TIMER:
                    if not self.paused:
                        self.clearPiece(self.activepiece)
                        if not self.board.validMoveDown(self.activepiece):
                            self.spawn = True

            # Prepare active piece for drawing
            self.clearPiece(self.shadowPiece)
            self.makeShadow()
            self.preparePiece(self.activepiece)

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

            # Draw everything
            self.next_box.drawChanges(C.disp)
            self.hold_box.drawChanges(C.disp)
            self.board.drawChanges(C.disp)
            levellabel = C.scoreFont.render("Level: "+str(self.level), 1, C.LIGHT_GREY)
            scorelabel = C.scoreFont.render("Score: "+str(self.score), 1, C.LIGHT_GREY)
            C.disp.blit(pygame.Surface((C.SCREEN_W, C.BOX_SIZE*2)), (0,0))
            C.disp.blit(levellabel, (C.SCREEN_W/2 - C.BOX_SIZE*5, 0))
            C.disp.blit(scorelabel, (C.SCREEN_W/2 - C.BOX_SIZE*5, C.BOX_SIZE))
            pygame.display.update()

