__author__ = 'Eric'

import pygame
import sys
from random import randint
from classes import *
from pygame.locals import *
from consts import *

pygame.init()
disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Netris v.0.1')

# TODO: Set up the playing board
board = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))

# TODO: Set up the next piece box

paused = False
spawn = True
location = [0,0]
pygame.time.set_timer(INPUT_TIMER, 50)
u_hold = d_hold = l_hold = r_hold = 3
up = down = left = right = False
u_first = d_first = l_first = r_first = False
while True:  # main game loop
    if spawn:
        nextPiece = randint(0,6)
        spawn = False
        activeblock = SheetedSprite(BLOCK_FILE,BLOCKS[nextPiece])

    for event in pygame.event.get():  # event handler
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
                    activeblock.rotate()
                if event.key == K_RCTRL:
                    spawn = True
            # TODO: P or ESC pauses
            if event.key == K_p or event.key == K_ESCAPE:
                paused = not paused

        # key was released
        if event.type == KEYUP:
            if event.key == K_UP:
                up = u_first = False
            if event.key == K_LEFT:
                left = l_first = False
            if event.key == K_RIGHT:
                right = r_first = False
            if event.key == K_DOWN:
                down = d_first = False
        if event.type == QUIT:  # exits the game safely
            pygame.quit()
            sys.exit()

        elif event.type == INPUT_TIMER:
            if not paused:
                if up:
                    if u_first or u_hold <= 0:
                        location[1] -= 24
                        if location[1] < 0: location[1] = 0
                        u_first = False
                    else: u_hold -= 1
                if left:
                    if l_first or l_hold <= 0:
                        location[0] -= 24
                        if location[0] < 0: location[0] = 0
                        l_first = False
                    else: l_hold -= 1
                if right:
                    if r_first or r_hold <= 0:
                        location[0] += 24
                        if location[0]+activeblock.width >= BOARD_WIDTH: location[0] = BOARD_WIDTH-activeblock.width
                        r_first = False
                    else: r_hold -= 1
                if down:
                    if d_first or d_hold <= 0:
                        location[1] += 24
                        if location[1]+activeblock.height >= BOARD_HEIGHT: location[1] = BOARD_HEIGHT-activeblock.height
                        d_first = False
                    else: d_hold -= 1

    # Perform events if keys are pressed
    #TODO: Determine if piece should stop moving
    #TODO: Determine if top boundary is breached
    board.fill(BLACK)
    board.blit(activeblock.image, location)

    disp.fill(BLACK)
    disp.blit(board, (SCREEN_WIDTH/2 - BOARD_WIDTH/2, 0))
    pygame.display.update()