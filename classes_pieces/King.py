import pygame
from pygame.locals import *
from classes_pieces.pieces import Piece
from board.constants import *

class King(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color, surface, row, col)
        self.name = 'king'
        self.has_moved = False
        self.is_checked = False
    def generate_moves(self, board):
        moves = []
        last_range = 7
        initial_range = 0
        offset_x = (self.row + 1 if self.row != last_range else self.row, self.row - 1 if self.row != initial_range else self.row ) #Esto posiblemente tenga errores, revisar
        offset_y = (self.col + 1 if self.col  != last_range else self.col, self.col - 1 if self.col != initial_range else self.col)

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(board[row][col],int):
                    if row in offset_x and col in offset_y: #Este for posiblemente tenga errores, revisar luego de correr
                        moves.append((row,col))