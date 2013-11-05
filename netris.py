__author__ = 'Eric'

import pygame
import sys
from pygame.locals import *
from random import shuffle
from consts import *
from classes import *

def clearPiece(p):
    for i, row in enumerate(p.matrix):
        for j, block in enumerate(row):
            if block != 'E':
                board.changeCell(i+p.coord[1], j+p.coord[0], 'E', None)

def preparePiece(p):
    offi = p.coord[1]
    offj = p.coord[0]
    for i,row in enumerate(p.matrix):
        for j,block in enumerate(p.matrix[i]):
            change = p.matrix[i][j]
            if change != 'E':
                board.changeCell(i+offi,j+offj,change,sprites.get(change).image)

# Playing board
board = Grid((SCREEN_W/2 - BOX_SIZE*5, BOX_SIZE/5), 10, 22)
board.drawChanges(disp)

# Next piece box
next_box = Grid((board.location[0] - BOX_SIZE*6, BOX_SIZE/5 + BOX_SIZE*2), 5, 5)
next_box.drawChanges(disp)

# Sprite array
sheet = pygame.image.load(BLOCK_FILE).convert()
sprites = {'I' : Block(sheet,'I'),
          'J' : Block(sheet,'J'),
          'L' : Block(sheet,'L'),
          'O' : Block(sheet,'O'),
          'S' : Block(sheet,'S'),
          'T' : Block(sheet,'T'),
          'Z' : Block(sheet,'Z')}

# Flags and other necessary variables
paused = False
spawn = True
pygame.time.set_timer(INPUT_TIMER, 50)
pygame.time.set_timer(DROP_TIMER, 1000)
u_hold = d_hold = l_hold = r_hold = 3
up = down = left = right = False
u_first = d_first = l_first = r_first = False
order = ['I','J','L','O','S','T','Z']
shuffle(order)
count = 0
nextpiece = Tetromino(order[count])

# Main game loop
while True:

    # Spawn a new piece, and determine the next piece
    if spawn:
        spawn = False
        activepiece = nextpiece
        count += 1
        if count > 6:
            count = 0
            shuffle(order)
        nextpiece = Tetromino(order[count])
        next_box.clear()
        # Draw next piece
        for i,row in enumerate(nextpiece.matrix):
            for j,block in enumerate(nextpiece.matrix[i]):
                if block != 'E':
                    next_box.changeCell(i+1,j+1,block,sprites.get(block).image)
                else:
                    next_box.changeCell(i+1,j+1,block,None)
        # Prepare active piece for drawing
        preparePiece(activepiece)


    # Event handler
    for event in pygame.event.get():
        # Register a key being pressed
        if event.type == KEYDOWN:
            if not paused:
                if event.key == K_UP:
                    clearPiece(activepiece)
                    while board.validMoveDown(activepiece) is not None: continue
                if event.key == K_LEFT:
                    left = l_first = True
                    l_hold = 3
                if event.key == K_RIGHT:
                    right = r_first = True
                    r_hold = 3
                if event.key == K_DOWN:
                    down = d_first = True
                    d_hold = 3
                if event.key == K_LCTRL:
                    for i, row in enumerate(activepiece.matrix):
                        for j, block in enumerate(row):
                            if block != 'E':
                                board.changeCell(i+activepiece.coord[1], j+activepiece.coord[0], 'E', None)
                    board.validRotLeft(activepiece)
                if event.key == K_RCTRL:
                    for i, row in enumerate(activepiece.matrix):
                        for j, block in enumerate(row):
                            if block != 'E':
                                board.changeCell(i+activepiece.coord[1], j+activepiece.coord[0], 'E', None)
                    board.validRotRight(activepiece)
                if event.key == K_SPACE:
                    spawn = True

            # Pause the game
            if event.key == K_p:
                paused = not paused
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Key was released
        if event.type == KEYUP:
            if event.key == K_LEFT:
                left = l_first = False
            if event.key == K_RIGHT:
                right = r_first = False
            if event.key == K_DOWN:
                down = d_first = False

        # Exits the game safely
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Move the piece (timer used to control the hold speed)
        if event.type == INPUT_TIMER:
            if not paused:
                clearPiece(activepiece)
                if left:
                    if l_first or l_hold <= 0:
                        w = activepiece.width
                        board.validMoveLeft(activepiece)
                        l_first = False
                    else: l_hold -= 1
                if right:
                    if r_first or r_hold <= 0:
                        board.validMoveRight(activepiece)
                        r_first = False
                    else: r_hold -= 1
                if down:
                    if d_first or d_hold <= 0:
                        board.validMoveDown(activepiece)
                        d_first = False
                    else: d_hold -= 1

        if event.type == DROP_TIMER:
            clearPiece(activepiece)
            if board.validMoveDown(activepiece) is None:
                spawn = True

    # Prepare active piece for drawing
    preparePiece(activepiece)

    # Check rows for clearing
    if spawn:
        for i in xrange(board.height):
            board.clearRow(i)

    # Draw everything
    next_box.drawChanges(disp)
    board.drawChanges(disp)
    pygame.display.update()
