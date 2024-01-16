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

        
        east = self.calc_rook_moves(self.col,COLS,1,board)
        west = self.calc_rook_moves(self.col,-1,-1,board)
        north = self.calc_rook_moves(self.row,-1,-1,board,exchange_rowNcol=True)
        south = self.calc_rook_moves(self.row,ROWS,1,board,exchange_rowNcol=True)
 
        moves = east + west + north + south

        return moves
    
    def calc_rook_moves(self,start,end,step, board,exchange_rowNcol = False):
        array_move = []
        if exchange_rowNcol:
            for row in range(start,end,step):
                if isinstance(board[self.col][row],int):
                    array_move.append((row,self.col))
        else:
            for col in range(start,end,step):
                if isinstance(board[self.row][col],int):
                    array_move.append((self.row,col))
        return array_move
