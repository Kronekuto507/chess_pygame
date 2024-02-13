import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from board.constants import *
from classes_pieces.Rook import Rook

class King(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color, surface, row, col)
        self.name = 'king'
        self.has_moved = False
        self.can_castle_array = None
        self.starting_coordinates = (0,4) if self.color == 'black' else (7,4)
        self.castling_squares = {7: (self.row,6), 0: (self.row,2)}
        self.has_castled = False

    def generate_moves(self, board):
        starter_row = self.row - 1
        later_row = self.row + 2
        starter_col = self.col - 1
        later_col = self.col + 2
        moves = []
        for row in range(starter_row,later_row):
            for col in range(starter_col,later_col):
                if row<= 7 and row >= 0 and col <= 7 and col>= 0:
                    if isinstance(board.virtual_board[row][col],int) or not board.is_ally_piece(self,board.virtual_board[row][col]):
                        moves.append((row,col))

        valid_moves = moves
        return valid_moves
    
    def get_rooks(self,board):
        pass
    
    def can_castle_m(self):
        return self.can_castle
    
    def clone(self):

        king = King(self.color,self.surface,self.row,self.col)
        king.has_moved = self.has_moved
        king.can_castle_array = self.can_castle_array
        return king
        
    
        

