import pygame
from pygame.locals import *
from game import Game

class Text:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = None
        self.color = Color(0,0,0)
        self.fontsize = 30
        self.render()
    
    def render(self):
        self.font = pygame.font.Font(None, self.fontsize)
        self.font.render(self.text)



    def draw():
        Game.screen.blit()
    
