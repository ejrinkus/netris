__author__ = 'Eric'

import pygame
import sys
from pygame.locals import *
from random import shuffle
from consts import *
from classes import *

# Initializers
pygame.init()
disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Netris v.0.1')

# Playing board
board = Grid((SCREEN_WIDTH/2 - BOARD_WIDTH/2, 5), 10, 22)
board.drawChanges(disp)

# Next piece box
next_box = Grid((60, 53), 5, 5)
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
        # Draw next piece
        for i in xrange(len(nextpiece.matrix)):
            for j in xrange(len(nextpiece.matrix[i])):
                change = nextpiece.matrix[i][j]
                if change != 'E':
                    next_box.changeCell(i+1,j+1,change,sprites.get(change).image)
                else:
                    next_box.changeCell(i+1,j+1,change,None)
        # Draw current piece
        for i in xrange(len(activepiece.matrix)):
            for j in xrange(len(activepiece.matrix[i])):
                change = activepiece.matrix[i][j]
                offi = activepiece.coord[1]
                offj = activepiece.coord[0]
                if change != 'E':
                    board.changeCell(i+offi,j+offj,change,sprites.get(change).image)
                else:
                    board.changeCell(i+offi,j+offj,change,None)

    # Event handler
    for event in pygame.event.get():
        # Register a key being pressed
        if event.type == KEYDOWN:
            if not paused:
                if event.key == K_UP:
                    up = u_first = True
                    u_hold = 3
                if event.key == K_LEFT:
                    left = l_first = True
                    l_hold = 3
                if event.key == K_RIGHT:
                    right = r_first = True
                    r_hold = 3
                if event.key == K_DOWN:
                    down = d_first = True
                    d_hold = 3
                if event.key == K_SPACE:
                    print 'rotate here'
                if event.key == K_RCTRL:
                    spawn = True
            # Pause the game
            if event.key == K_p or event.key == K_ESCAPE:
                paused = not paused

        # Key was released
        if event.type == KEYUP:
            if event.key == K_UP:
                up = u_first = False
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

        # Move the piece (timer used to slow down the speed if the key is held down)
        if event.type == INPUT_TIMER:
            if not paused:
                if up:
                    if u_first or u_hold <= 0:
                        #TODO
                        u_first = False
                    else: u_hold -= 1
                if left:
                    if l_first or l_hold <= 0:
                        #TODO
                        l_first = False
                    else: l_hold -= 1
                if right:
                    if r_first or r_hold <= 0:
                        #TODO
                        r_first = False
                    else: r_hold -= 1
                if down:
                    if d_first or d_hold <= 0:
                        #TODO
                        d_first = False
                    else: d_hold -= 1

    next_box.drawChanges(disp)
    board.drawChanges(disp)
    pygame.display.update()


