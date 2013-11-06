__author__ = 'Eric'

import pygame, copy
from consts import *

# Class to display each individual block
# id: Shape the block belongs to (determines color, too)
# image: Drawable image for the block
class Block(pygame.sprite.Sprite):
    # Constructor
    # sheet: image object for the sprite sheet
    # rect_set: set of rotations for the block
    def __init__(self, sheet, t):
        super(Block, self).__init__()
        rect = pygame.Rect(SPRITE_COORD.get(t))
        self.id = t
        self.image = pygame.Surface(rect.size).convert()
        self.image.blit(sheet, (0, 0), rect)

# Class representing a tetromino using a char matrix
# matrix: matrix representing orientation and shape of tetromino
# id: Type of tetromino
class Tetromino(object):

    # Constructor
    # t: Type of tetromino
    def __init__(self, t='E'):
        if t == 'E':
            self.matrix = (('E','E'),('E','E'))
            self.coord = [0,0]
        else:
            self.matrix = BLOCKS.get(t)
            self.coord = [3,0]
        self.id = t
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)
        self.state = 0
        if t == 'I':
            self.kicks = (((0,0),(2,0),(-1,0),(2,-1),(-1,2)),
                          ((0,0),(-2,0),(-1,0),(-2,-1),(1,2)),
                          ((0,0),(-2,0),(1,0),(-2,-1),(1,1)),
                          ((0,0),(-2,0),(1,0),(1,-2),(-2,1)),
                          ((0,0),(1,0),(-2,0),(1,-2),(-2,1)),
                          ((0,0),(-1,0),(2,0),(-1,-2),(2,1)),
                          ((0,0),(2,0),(-1,0),(-1,-2),(2,1)),
                          ((0,0),(2,0),(-1,0),(2,-1),(-1,1)))

        else :
            self.kicks = (((0,0),(1,0),(1,1),(0,-2),(1,-2)),
                          ((0,0),(-1,0),(-1,1),(0,-2),(-1,-2)),
                          ((0,0),(-1,0),(-1,-1),(0,2),(-1,2)),
                          ((0,0),(-1,0),(-1,-1),(0,2),(-1,2)),
                          ((0,0),(-1,0),(-1,1),(0,-2),(-1,-2)),
                          ((0,0),(1,0),(1,1),(0,-2),(1,-2)),
                          ((0,0),(1,0),(1,-1),(0,2),(1,2)),
                          ((0,0),(1,0),(1,-1),(0,2),(1,2)))

    # Rotate the tetromino clockwise
    def rotateRight(self):
        self.matrix = zip(*self.matrix[::-1])
        self.state += 1
        if self.state == 4:
            self.state = 0

    # Rotate the tetromino counterclockwise
    def rotateLeft(self):
        self.matrix = zip(*self.matrix)[::-1]
        self.state -= 1
        if self.state == -1:
            self.state = 3

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
        self.width = width
        self.height = height
        for i in xrange(height):
            self.grid.append([])
            for j in xrange(width):
                self.grid[i].append(Cell(i in hide))
                self.changed.append((i,j))

    # Clear out every cell in the grid
    def clear(self):
        for i,row in enumerate(self.grid):
            for j,block in enumerate(row):
                self.changeCell(i,j,'E',None)

    # Check a row and clear it if it is full
    # low: index of the row to cehck
    def clearRow(self,row):
        # Check the row
        for block in self.grid[row]:
            if block.contents == 'E': return
        # Copy all rows obove it downward to clear it
        for i,r in reversed(list(enumerate(self.grid))):
            if i > row: continue
            for j,block in enumerate(r):
                if i == 0:
                    self.changeCell(i,j,'E',None)
                else:
                    self.changeCell(i,j,self.grid[i-1][j].contents,self.grid[i-1][j].surface)

    # Change the contents of a cell in the grid.  Tracks the cell for future drawing.
    # row: row of the cell
    # col: col of the cell
    # c: new type for the cell
    # sprite: sprite to draw to the cell
    def changeCell(self, row, col, c, sprite):
        if not (0 <= row < self.height and 0 <= col < self.width) or self.grid[row][col].contents == c:
            return
        self.grid[row][col].setContents(c)
        x = BOX_SIZE-1
        if sprite is not None:
            sprite = pygame.transform.scale(sprite, (BOX_SIZE, BOX_SIZE))
            self.grid[row][col].surface.blit(sprite, (0,0))
        else:
            self.grid[row][col].surface.fill(BLACK)
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

    # Returns the altered Tetromino if the movement is valid, or None if not. (for all below functions)
    # tetromino: Tetromino object being moved

    # move down
    def validMoveDown(self, tetromino):
        for i,row in enumerate(tetromino.matrix):
            # Break if the last row is at the bottom of the grid AND contains part of the tetromino
            if i+tetromino.coord[1] >= self.height-1 and tetromino.id in row:
                break
            for j,block in enumerate(tetromino.matrix[i]):
                # Continue if the block is empty or if the block below is part of the tetromino
                if block == 'E': continue
                if i < tetromino.height-1 and tetromino.matrix[i+1][j] != 'E': continue
                # Break if there is a block in the way
                pos = self.grid[i+tetromino.coord[1]+1][j+tetromino.coord[0]].contents
                if pos != 'E':
                    break
            else:
                continue
            break
        else:
            tetromino.coord[1] += 1
            return tetromino
        return None

    # move left
    def validMoveLeft(self, tetromino):
        for i,row in enumerate(tetromino.matrix):
            for j,block in enumerate(tetromino.matrix[i]):
                # Continue if the block is empty or if the block to the left is part of the tetromino
                if block == 'E': continue
                # Break if the tetromino is at the side
                if j+tetromino.coord[0] <= 0: break
                if j > 0 and tetromino.matrix[i][j-1] != 'E': continue
                # Break if there is a block in the way
                pos = self.grid[i+tetromino.coord[1]][j+tetromino.coord[0]-1].contents
                if pos != 'E': break
            else:
                continue
            break
        else:
            tetromino.coord[0] -= 1
            return tetromino
        return None

    # move up
    def validMoveUp(self, tetromino):
        for i,row in enumerate(tetromino.matrix):
            # Break if the first row is at the top of the grid AND contains part of the tetromino
            if i+tetromino.coord[1] <= 0 and tetromino.id in row:
                break
            for j,block in enumerate(tetromino.matrix[i]):
                # Continue if the block is empty or if the block above is part of the tetromino
                if block == 'E': continue
                if i > 0 and tetromino.matrix[i-1][j] != 'E': continue
                # Break if there is a block in the way
                pos = self.grid[i+tetromino.coord[1]-1][j+tetromino.coord[0]].contents
                if pos != 'E': break
            else:
                continue
            break
        else:
            tetromino.coord[1] -= 1
            return tetromino
        return None

    # move right
    def validMoveRight(self, tetromino):
        for i,row in enumerate(tetromino.matrix):
            for j,block in enumerate(tetromino.matrix[i]):
                # Continue if the block is empty or if the block to the right is part of the tetromino
                if block == 'E': continue
                # Break if the tetromino is at the side
                if j+tetromino.coord[0] >= self.width-1: break
                if j < tetromino.width-1 and tetromino.matrix[i][j+1] != 'E': continue
                # Break if there is a block in the way
                pos = self.grid[i+tetromino.coord[1]][j+tetromino.coord[0]+1].contents
                if pos != 'E': break
            else:
                continue
            break
        else:
            tetromino.coord[0] += 1
            return tetromino
        return None

    def validRotRight(self, tetromino):
        tetromino.rotateRight()
        kicks = tetromino.kicks[tetromino.state*2 + 1]
        for i in xrange(5):
            tetromino.coord[0] += kicks[i][0]
            tetromino.coord[1] += kicks[i][1]
            for j,row in enumerate(tetromino.matrix):
                for k,block in enumerate(tetromino.matrix[j]):
                    if block == 'E': continue
                    if j+tetromino.coord[1] < 0 or j+tetromino.coord[1] >= self.height: break
                    if k+tetromino.coord[0] < 0 or k+tetromino.coord[0] >= self.width: break
                    if self.grid[j+tetromino.coord[1]][k+tetromino.coord[0]].contents != 'E': break

                else:
                    continue
                break
            else:
                return tetromino
            tetromino.coord[0] -= kicks[i][0]
            tetromino.coord[1] -= kicks[i][1]
        tetromino.rotateLeft()
        return tetromino



    def validRotLeft(self, tetromino):
        tetromino.rotateLeft()
        kicks = tetromino.kicks[tetromino.state*2]
        for i in xrange(5):
            tetromino.coord[0] += kicks[i][0]
            tetromino.coord[1] += kicks[i][1]
            for j,row in enumerate(tetromino.matrix):
                for k,block in enumerate(tetromino.matrix[j]):
                    if block == 'E': continue
                    if j+tetromino.coord[1] < 0 or j+tetromino.coord[1] >= self.height: break
                    if k+tetromino.coord[0] < 0 or k+tetromino.coord[0] >= self.width: break
                    if self.grid[j+tetromino.coord[1]][k+tetromino.coord[0]].contents != 'E': break

                else:
                    continue
                break
            else:
                return tetromino
            tetromino.coord[0] -= kicks[i][0]
            tetromino.coord[1] -= kicks[i][1]
        tetromino.rotateRight()
        return tetromino
