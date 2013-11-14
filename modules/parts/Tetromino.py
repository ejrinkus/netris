################################################################################
#
#  Contains the Tetromino class.  This is used to form the shape of a tetromino,
#  and contains the proper rendering block for that particular tetromino.
#
################################################################################

__author__ = 'Eric'

from modules.parts.Block import Block

# Default block orientations
BLOCKS = { 'I' : (('E','E','E','E'),
                  ('I','I','I','I'),
                  ('E','E','E','E'),
                  ('E','E','E','E')),

           'J' : (('J','E','E'),
                  ('J','J','J'),
                  ('E','E','E')),

           'L' : (('E','E','L'),
                  ('L','L','L'),
                  ('E','E','E')),

           'O' : (('E','O','O','E'),
                  ('E','O','O','E'),
                  ('E','E','E','E')),

           'S' : (('E','S','S'),
                  ('S','S','E'),
                  ('E','E','E')),

           'T' : (('E','T','E'),
                  ('T','T','T'),
                  ('E','E','E')),

           'Z' : (('Z','Z','E'),
                  ('E','Z','Z'),
                  ('E','E','E'))}

# Class representing a tetromino using a char matrix
# matrix: matrix representing orientation and shape of tetromino
# id: Type of tetromino
# shadow: If the blocks are shadow blocks, this is true
# coord: location of top-left corner relative to its grid
# block: object representing types of blocks in this piece
# width: total width of the piece's matrix
# height: total height of the piece's matrix
# state: rotational state of the piece
# kicks: shift values for kick rotations
class Tetromino(object):

    # Constructor
    # t: Type of tetromino
    def __init__(self, t='E', shadow=False):
        self.shadow = shadow
        if t == 'E':
            self.matrix = (('E',),)
            self.block = None
            self.coord = [0,0]
        else:
            self.matrix = BLOCKS.get(t)
            self.block = Block(t,shadow)
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
