__author__ = 'Eric'

import pygame
from consts import *

# Class to display each individual block
# id: Shape the block belongs to (determines color, too)
# image: Drawable image for the block
class Block(pygame.sprite.Sprite):
    # Constructor
    # sheet: image object for the sprite sheet
    # rect_set: set of rotations for the block
    def __init__(self, sheet, type):
        rect = pygame.Rect(SPRITE_COORD.get(type))
        self.id = type
        self.image = pygame.Surface(rect.size).convert()
        self.image.blit(sheet, (0, 0), rect)

# Class representing a tetromino using a char matrix
# matrix: matrix representing orientation and shape of tetromino
# id: Type of tetromino
class Tetromino(object):
    # Constructor
    # t: Type of tetromino
    def __init__(self, t):
        self.matrix = BLOCKS.get(t)
        self.id = t
        self.coord = (3,0)

    # Rotate the tetromino clockwise
    def rotateRight(self):
        self.matrix = zip(*self.matrix[::-1])

    # Rotate the tetromino counterclockwise
    def rotateLeft(self):
        self.matrix = zip(*self.matrix)[::-1]

# Class representing a single cell of a grid
# surface: surface upon which the contents of the cell may be drawn
# contents: represent what the cell contains
class Cell(object):
    # Constructor
    def __init__(self, hidden = False):
        x = BOX_SIZE-1
        self.surface = pygame.Surface((BOX_SIZE,BOX_SIZE))
        self.contents = 'E'
        self.hidden = hidden
        if not hidden:
            pygame.draw.line(self.surface, GREY, (0,0), (0,x), 1)
            pygame.draw.line(self.surface, GREY, (x,0), (x,x), 1)
            pygame.draw.line(self.surface, GREY, (0,0), (x,0), 1)
            pygame.draw.line(self.surface, GREY, (0,x), (x,x), 1)

    # Changes the contents of the cell
    # c: new contents of the cell
    def setContents(self, c):
        self.contents = c

    # Toggles whether or not the cell is hidden
    def toggleHidden(self):
        self.hidden = not self.hidden

# Class representing a grid
# grid: 2-D array of cell objects representing this grid
# location: coordinates of the upper left hand corner of the grid, relative to the main display
# changed: cells that have changed and haven't been drawn yet
# surf: surface this grid is drawn to
class Grid(object):
    # Constructor
    # coord: initial value of location
    # width: number of columns in the grid
    # height: number of rows in the grid
    # s: surface this grid is drawn to
    # hide: rows to hide
    def __init__(self, coord, width, height, hide = ()):
        self.location = coord
        self.changed = []
        self.grid = []
        for i in xrange(height):
            self.grid.append([])
            for j in xrange(width):
                self.grid[i].append(Cell(i in hide))
                self.changed.append((i,j))

    # Change the contents of a cell in the grid.  Tracks the cell for future drawing.
    # row: row of the cell
    # col: col of the cell
    # c: new type for the cell
    # sprite: sprite to draw to the cell
    def changeCell(self, row, col, c, sprite):
        if self.grid[row][col].contents == c: return
        self.grid[row][col].setContents(c)
        x = BOX_SIZE-1
        if sprite != None:
            sprite = pygame.transform.scale(sprite, (BOX_SIZE, BOX_SIZE))
            self.grid[row][col].surface.blit(sprite, (0,0))
        else:
            pygame.draw.line(self.grid[row][col].surface, GREY, (0,0), (0,x), 1)
            pygame.draw.line(self.grid[row][col].surface, GREY, (x,0), (x,x), 1)
            pygame.draw.line(self.grid[row][col].surface, GREY, (0,0), (x,0), 1)
            pygame.draw.line(self.grid[row][col].surface, GREY, (0,x), (x,x), 1)
        if (row,col) not in self.changed: self.changed.append((row,col))

    # Draws any changed cells to the given surface
    # surf: surface to be drawn to
    def drawChanges(self, surf):
        x = BOX_SIZE-1
        for (row,col) in self.changed:
            surf.blit(self.grid[row][col].surface, (col*x+self.location[0], row*x+self.location[1]))
        self.changed = []
