import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from board.constants import *

class King(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color, surface, row, col)
        self.name = 'king'
        self.has_moved = False
        self.is_checked = False
        self.castling_queen_side = (self.row,self.col - 2)
        self.castling_king_side = (self.row,self.col + 2)
    def generate_moves(self, board):
        starter_row = self.row - 1
        later_row = self.row + 2
        starter_col = self.col - 1
        later_col = self.col + 2
        moves = []
        for row in range(starter_row,later_row):
            for col in range(starter_col,later_col):
                if row<= 7 and row >= 0 and col <= 7 and col>= 0:
                    if isinstance(board.virtual_board[row][col],int):
                        moves.append((row,col))
                        if self.has_moved == False:
                            moves.append((self.row,self.col + 2 ))
                            moves.append((self.row,self.col - 2))
        return moves
    
        

