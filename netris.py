__author__ = 'Eric'

from header import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Netris v.0.1')
# TODO: Load the block spritesheet (use the sprite module from pygame)

# TODO: Set up the playing board
# TODO: Set up the next piece box

while True: # main game loop
    #TODO: Decide if next piece should spawn
    #TODO: Determine next piece (and display in box)

    for event in pygame.event.get(): # event handler
        #TODO: Up arrow rotates
        #TODO: Left/right arrows shift
        #TODO: Down arrow drops faster
        #TODO: Space instant drops
        #TODO: P or ESC pauses
        if event.type == QUIT: # exits the game safely
            pygame.quit()
            sys.exit()

    #TODO: Determine if piece should stop moving
    #TODO: Determine if top boundary is breached
    pygame.display.update()