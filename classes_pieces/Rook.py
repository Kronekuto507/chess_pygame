import pygame
from pygame.locals import *
from board.constants import *
from classes_pieces.pieces import Piece

class Rook(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'rook'
        self.is_moved  = False

    def generate_moves(self,board):

        offsett = (COLS * -1) + self.col
        later_offsett = (COLS * -1)

        east = []

        for col in range(self.col, COLS + 1):
            if isinstance(board[self.row][col],int):
                east.append((self.row,col))
            else:
                break

        west = []

        for col in range(offsett, later_offsett + 1):
            if isinstance(board[self.row][col], int):
                west.append((self.row, COLS + col))
        
        vertical = []

        for col in range(COLS):
            for row in range(ROWS):
                if col == self.col:
                    if isinstance(board[row][col],int):
                        vertical.append(row,col)
                        
        moves = east + west + vertical

        return moves