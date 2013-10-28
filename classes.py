__author__ = 'Eric'

import pygame
import sys
from pygame.locals import *
from consts import *

class SheetedSprite(pygame.sprite.Sprite):

    # Constructor
    # filename: filename of the sprite sheet
    # rect_set: set of rotations for the block
    def __init__(self, filename, rect_set):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load sprite sheet image:', filename
            raise SystemExit, message
        self.set = rect_set
        self.rot = 0
        self.rect = self.set[self.rot]
        self.image = self.image_at(self.rect)
        self.width = self.rect[2]+1
        self.height = self.rect[3]+1

    # Load a specific image from a specific rectangle
    # rectangle: image boundary
    # colorkey: transparency color (R,G,B)
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

    # Rotate the sprite 90 degrees clockwise
    def rotate(self):
        self.rot += 1
        if self.rot >= len(self.set):
            self.rot = 0
        self.rect = self.set[self.rot]
        self.image = self.image_at(self.rect)
        self.width = self.rect[2]+1
        self.height = self.rect[3]+1
