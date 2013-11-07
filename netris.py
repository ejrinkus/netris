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
    drawCoords = []
    for i,row in enumerate(p.matrix):
        for j,block in enumerate(p.matrix[i]):
            if block != 'E':
                if(board.grid[i+offi][j+offj].contents == 'E'): drawCoords.append((i+offi,j+offj))
                else: return False
    for coord in drawCoords:
        board.changeCell(coord[0],coord[1],p.id,sprites.get(p.id).image)
    return True

def exitGame():
    pygame.quit()
    sys.exit()


# Playing board
board = Grid((SCREEN_W/2 - BOX_SIZE*5, BOX_SIZE/5), 10, 22, (0,1))
board.drawChanges(disp)

# Next piece box
next_box = Grid((board.location[0] - BOX_SIZE*6, BOX_SIZE/5 + BOX_SIZE*2), 5, 5)
next_box.drawChanges(disp)

# Hold box
hold_box = Grid((board.location[0] + BOX_SIZE*11, BOX_SIZE/5 + BOX_SIZE*2), 5, 5)
hold_box.drawChanges(disp)

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
hold = False
hold_flag = False
pygame.time.set_timer(INPUT_TIMER, 50)
pygame.time.set_timer(DROP_TIMER, 1000)
u_hold = d_hold = l_hold = r_hold = 3
up = down = left = right = False
u_first = d_first = l_first = r_first = False
order = ['I','J','L','O','S','T','Z']
shuffle(order)
count = 0
nextpiece = Tetromino(order[count])
heldpiece = Tetromino()
cleared = 0
timeFlag = False
speed = 1000.0
score = 0
level = 1
font = pygame.font.SysFont("monospace",24)

# Main game loop
while True:

    if timeFlag:
        timeFlag = False
        speed *= 0.9
        level += 1
        pygame.time.set_timer(DROP_TIMER, int(speed))

    # Switch out the held piece
    if hold:
        hold = hold_flag = False
        clearPiece(activepiece)
        temp = activepiece.id
        activepiece = Tetromino(heldpiece.id)
        heldpiece = Tetromino(temp)
        # Draw held piece
        hold_box.clear()
        for i,row in enumerate(heldpiece.matrix):
            for j,block in enumerate(row):
                if block != 'E':
                    hold_box.changeCell(i+1,j+1,block,sprites.get(block).image)
                else:
                    hold_box.changeCell(i+1,j+1,block,None)
        # Prepare active piece for drawing (or spawn new piece if there was no held piece)
        if activepiece.id != 'E':
            preparePiece(activepiece)
        else:
            spawn = True

    # Spawn a new piece, and determine the next piece
    if spawn:
        spawn = False
        hold_flag = True
        activepiece = nextpiece
        count += 1
        if count > 6:
            count = 0
            shuffle(order)
        nextpiece = Tetromino(order[count])
        next_box.clear()
        # Draw next piece
        for i,row in enumerate(nextpiece.matrix):
            for j,block in enumerate(row):
                if block != 'E':
                    next_box.changeCell(i+1,j+1,block,sprites.get(block).image)
                else:
                    next_box.changeCell(i+1,j+1,block,None)
        # Prepare active piece for drawing
        if not preparePiece(activepiece):
            exitGame()

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
                if event.key == K_LCTRL and activepiece.id != 'O':
                    for i, row in enumerate(activepiece.matrix):
                        for j, block in enumerate(row):
                            if block != 'E':
                                board.changeCell(i+activepiece.coord[1], j+activepiece.coord[0], 'E', None)
                    board.validRotLeft(activepiece)
                if event.key == K_RCTRL and activepiece.id != 'O':
                    for i, row in enumerate(activepiece.matrix):
                        for j, block in enumerate(row):
                            if block != 'E':
                                board.changeCell(i+activepiece.coord[1], j+activepiece.coord[0], 'E', None)
                    board.validRotRight(activepiece)
                if event.key == K_SPACE and hold_flag == True:
                    hold = True

            # Pause the game
            if event.key == K_p:
                paused = not paused
            if event.key == K_ESCAPE:
                exitGame()

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
            exitGame()

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
            if not paused:
                clearPiece(activepiece)
                if board.validMoveDown(activepiece) is None:
                    spawn = True

    # Prepare active piece for drawing
    preparePiece(activepiece)

    # Check rows for clearing
    if spawn:
        temp = 0
        for i in xrange(board.height):
            if board.clearRow(i):
                cleared += 1
                temp += 1
                if cleared % 10 == 0: timeFlag = True
        if temp == 1:
            score += 100*level
        elif temp == 2:
            score += 300*level
        elif temp == 3:
            score += 500*level
        elif temp == 4:
            score += 800*level

    # Draw everything
    next_box.drawChanges(disp)
    hold_box.drawChanges(disp)
    board.drawChanges(disp)
    levellabel = font.render("Level: "+str(level), 1, LIGHT_GREY)
    scorelabel = font.render("Score: "+str(score), 1, LIGHT_GREY)
    disp.blit(pygame.Surface((SCREEN_W,BOX_SIZE*2)),(0,0))
    disp.blit(levellabel,(SCREEN_W/2-BOX_SIZE*5,0))
    disp.blit(scorelabel,(SCREEN_W/2-BOX_SIZE*5,BOX_SIZE))
    pygame.display.update()
