__author__ = 'Eric'

import pygame
import eztext
from pygame.locals import *
from game.consts import *

class OptionsMenu:

    def __init__(self):

        # Set up volume option
        self.volumeLabel = scoreFont.render("Volume: ", False, LIGHT_GREY)
        self.volMinus = scoreFont.render(" - ", False, LIGHT_GREY)
        self.volVal = scoreFont.render(GAME_DATA["Volume"][0], False, LIGHT_GREY)
        self.volPlus = scoreFont.render(" + ", False, LIGHT_GREY)

        totalWidth = self.volMinus.get_width() + self.volPlus.get_width() +\
                     self.volumeLabel.get_width() + self.volVal.get_width()
        totaHeight = self.volMinus.get_height()

        self.volumeRect = pygame.Rect((SCREEN_W/2 - totalWidth/2, SCREEN_H/2 - totaHeight),
                                      (self.volumeLabel.get_width(), self.volumeLabel.get_height()))
        self.minusRect = pygame.Rect(self.volumeRect.topright,
                                      (self.volMinus.get_width(), self.volMinus.get_height()))
        self.volValRect = pygame.Rect(self.minusRect.topright,
                                      (self.volVal.get_width(), self.volVal.get_height()))
        self.plusRect = pygame.Rect(self.volValRect.topright,
                                      (self.volPlus.get_width(), self.volPlus.get_height()))

        # Set up name option
        self.playerLabel = scoreFont.render("Player Name: ", False, LIGHT_GREY)
        self.nameLabel = scoreFont.render(GAME_DATA["User Name"][0], False, LIGHT_GREY)

        totalWidth = self.playerLabel.get_width() + self.nameLabel.get_width()
        totaHeight = self.playerLabel.get_height()

        self.playerRect = pygame.Rect((SCREEN_W/2 - totalWidth/2, SCREEN_H/2 + totaHeight/2),
                                      (self.playerLabel.get_width(), self.playerLabel.get_height()))
        self.nameRect = pygame.Rect(self.playerRect.topright,
                                      (self.nameLabel.get_width(), self.nameLabel.get_height()))
        self.textbox = eztext.Input(maxlength=15, color=WHITE)
        self.textbox.x = self.nameRect.left
        self.textbox.y = self.nameRect.top
        self.textbox.font = scoreFont
        self.textbox.value = GAME_DATA["User Name"][0]
        self.focusinput = False

    def draw(self):
        # Clear Screen
        disp.fill(BLACK)

        # Draw Text
        disp.blit(self.volumeLabel, (self.volumeRect.left, self.volumeRect.top))
        disp.blit(self.volMinus, (self.minusRect.left, self.minusRect.top))
        disp.blit(self.volVal, (self.volValRect.left, self.volValRect.top))
        disp.blit(self.volPlus, (self.plusRect.left, self.plusRect.top))
        disp.blit(self.playerLabel, (self.playerRect.left, self.playerRect.top))

        if self.focusinput:
            self.textbox.draw(disp)
        else:
            disp.blit(self.nameLabel, (self.nameRect.left, self.nameRect.top))

        pygame.display.update()

    def main(self):
        # Render loop
        while True:

            self.draw()

            # Input Loop
            events = pygame.event.get()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:

                    # Clicked Volume Down
                    if self.minusRect.collidepoint(event.pos) and not self.focusinput:
                        temp = int(GAME_DATA["Volume"][0])
                        temp -= 1
                        if temp < 0: temp = 0
                        GAME_DATA["Volume"][0] = str(temp)
                        self.volVal = scoreFont.render(GAME_DATA["Volume"][0], False, LIGHT_GREY)

                    # Clicked Volume Up
                    if self.plusRect.collidepoint(event.pos) and not self.focusinput:
                        temp = int(GAME_DATA["Volume"][0])
                        temp += 1
                        if temp > 10: temp = 10
                        GAME_DATA["Volume"][0] = str(temp)
                        self.volVal = scoreFont.render(GAME_DATA["Volume"][0], False, LIGHT_GREY)

                    # Clicked Name
                    if self.nameRect.collidepoint(event.pos):
                        self.focusinput = True

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    if self.focusinput:
                        self.focusinput = False
                        self.textbox.value = GAME_DATA["User Name"][0]
                    else:
                        disp.fill(BLACK)
                        return

                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.focusinput = False
                    GAME_DATA["User Name"][0] = self.textbox.value
                    self.nameLabel = scoreFont.render(GAME_DATA["User Name"][0], False, LIGHT_GREY)

            if self.focusinput:
                self.textbox.update(events)



