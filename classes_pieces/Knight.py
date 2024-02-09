import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from board.constants import *

class Knight(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'knight'
    def generate_moves(self,board):
        offsett = [(2,1),(2,-1),(1,2),(-1,2),(-2,1),(-2,-1),(1,-2),(-1,-2)]
        moves = []
        for tuple in offsett:
            row = self.row + tuple[0]
            col = self.col + tuple[1]
            if row >= 0 and row <= 7 and col >= 0 and col <= 7:
                if isinstance(board.virtual_board[row][col], int) or not board.is_ally_piece(self,board.virtual_board[row][col]):
                    moves.append((row,col))
        return moves
    
    def clone(self):
        return Knight(self.color,self.surface,self.row,self.col)
                    


