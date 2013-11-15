################################################################################
#
#  Contains the Grid class.  This is used for the playing board, next piece box,
#  hold piece box, and other tetromino displaying containers.  Also contains
#  various helper methods for moving and drawing pieces within the grid.
#
################################################################################
from game.Cell import Cell
from game.Tetromino import Tetromino

__author__ = 'Eric'

import pygame
from game.consts import *

# Class representing a grid
# grid: 2-D array of cell objects representing this grid
# location: coordinates of the upper left hand corner of the grid, relative to the main display
# changed: cells that have changed and haven't been drawn yet
# width: width in cells of this grid
# height: height in cells of this grid
class Grid(object):
    # Constructor
    # coord: initial value of location
    # width: number of columns in the grid
    # height: number of rows in the grid
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
                self.clearCell(i,j)

    # Check a row and clear it if it is full
    # row: index of the row to cehck
    def clearRow(self,row):
        # Check the row
        for block in self.grid[row]:
            if block.contents == 'E': return False
        # Copy all rows obove it downward to clear it
        for i,r in reversed(list(enumerate(self.grid))):
            if i > row: continue
            for j,block in enumerate(r):
                if i == 0 or self.grid[i-1][j].contents == 'E':
                    self.clearCell(i,j)
                else:
                    self.grid[i][j].surface.blit(self.grid[i-1][j].surface, (0,0))
                    self.grid[i][j].contents = self.grid[i-1][j].contents
                    if (i,j) not in self.changed: self.changed.append((i,j))
        return True

    # Clear the contents of a given cell
    # (row,col): coordinates of the cell to clear
    def clearCell(self, row, col):
        x = BOX_SIZE-1
        self.grid[row][col].contents = 'E'
        self.grid[row][col].surface.fill(BLACK)
        pygame.draw.line(self.grid[row][col].surface, GREY, (0,0), (0,x), 1)
        pygame.draw.line(self.grid[row][col].surface, GREY, (x,0), (x,x), 1)
        pygame.draw.line(self.grid[row][col].surface, GREY, (0,0), (x,0), 1)
        pygame.draw.line(self.grid[row][col].surface, GREY, (0,x), (x,x), 1)
        if (row,col) not in self.changed: self.changed.append((row,col))

    # Draw a given piece to the grid
    # piece: piece to draw
    # lock: true if this piece should be locked in place
    def drawPiece(self,piece,lock=False):
        for i,row in enumerate(piece.matrix):
            for j,val in enumerate(row):
                if val != 'E':
                    self.grid[i+piece.coord[1]][j+piece.coord[0]].surface.blit(piece.block.image, (0,0))
                    self.changed.append((i+piece.coord[1],j+piece.coord[0]))
                    if lock: self.grid[i+piece.coord[1]][j+piece.coord[0]].contents = val
        return True

    # Draw the shadow of a piece
    # piece: shadow to draw
    def drawShadow(self,piece):
        # Copy the data from the piece into its shadow
        shadow = Tetromino(piece.id,True)
        shadow.coord[0] = piece.coord[0]
        shadow.coord[1] = piece.coord[1]
        while shadow.state != piece.state:
            shadow.rotateRight()

        # Move the shadow as far down as possible
        while self.validMoveDown(shadow): continue

        # Draw the shadow (offi is how many cell the shadow is below its piece)
        offi = shadow.coord[1]-piece.coord[1]
        for i,row in enumerate(shadow.matrix):
            for j,val in enumerate(row):
                if 0 <= i+offi < piece.height and piece.matrix[i+offi][j] != 'E': continue
                if val != 'E':
                    self.grid[i+shadow.coord[1]][j+shadow.coord[0]].surface.blit(shadow.block.image, (0,0))
                    self.changed.append((i+shadow.coord[1],j+shadow.coord[0]))

    # Clear the shadow of a piece
    # piece: piece whose shadow to erase
    # (See comments for drawShadow for more details)
    def clearShadow(self,piece):
        shadow = Tetromino(piece.id,True)
        shadow.coord[0] = piece.coord[0]
        shadow.coord[1] = piece.coord[1]
        while shadow.state != piece.state:
            shadow.rotateRight()

        while self.validMoveDown(shadow): continue

        offi = shadow.coord[1]-piece.coord[1]
        for i,row in enumerate(shadow.matrix):
            for j,val in enumerate(row):
                if 0 <= i+offi < piece.height and piece.matrix[i+offi][j] != 'E': continue
                if val != 'E':
                    self.clearCell(i+shadow.coord[1], j+shadow.coord[0])
                    self.changed.append((i+shadow.coord[1],j+shadow.coord[0]))

    # Draws any changed cells to the given surface
    # surf: surface to be drawn to
    def drawChanges(self, surf):
        x = BOX_SIZE-1
        for (row,col) in self.changed:
            if self.grid[row][col].hidden: continue
            surf.blit(self.grid[row][col].surface, (col*x+self.location[0], row*x+self.location[1]))
        self.changed = []

    # Returns True if the movement is valid, or False if not. (for all below functions)
    # tetromino: Tetromino object being moved

    # in place
    def validPos(self, tetromino):
        for i,row in enumerate(tetromino.matrix):
            for j,block in enumerate(tetromino.matrix[i]):
                posi = i+tetromino.coord[1]
                posj = j+tetromino.coord[0]

                # Break if there is a block in the way or outside grid
                if posi < 0 or posi >= self.height or posj < 0 or posj >= self.width or\
                    self.grid[posi][posj].contents != 'E':
                    break
            else:
                continue
            break
        else:
            return True
        return False


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
                if self.grid[i+tetromino.coord[1]+1][j+tetromino.coord[0]].contents != 'E':
                    break
            else:
                continue
            break
        else:
            tetromino.coord[1] += 1
            return True
        return False

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
            return True
        return False

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
            return True
        return False

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
            return True
        return False

    # rotate right
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

    # rotate left
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
