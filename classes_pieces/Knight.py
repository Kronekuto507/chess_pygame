import pygame
from pygame.locals import *
from classes_pieces.pieces import Piece

class Knight(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'knight'