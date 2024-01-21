import pygame
from pygame.locals import *
from board.constants import *
from classes_pieces.Piece import Piece

class Rook(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'rook'
        self.has_moved  = False

    def generate_moves(self,board):

        east = self.calc_rook_moves(self.col,COLS,1,board)
        west = self.calc_rook_moves(self.col,-1,-1,board)
        north = self.calc_rook_moves(self.row,-1,-1,board,exchange_rowNcol=True)
        south = self.calc_rook_moves(self.row,ROWS,1,board,exchange_rowNcol=True)
 
        moves = east + west + north + south

        return moves
    
    def calc_rook_moves(self,start,end,step,board,exchange_rowNcol = False):
        array_move = []
        if exchange_rowNcol:
            for row in range(start,end,step):
                if isinstance(board.virtual_board[row][self.col],int):
                    array_move.append((row,self.col)) #Que carajo era ese error lols
                else:
                    if row != self.row:
                        if isinstance(board.virtual_board[row][self.col],Piece):
                            if board.is_ally_piece(self,board.virtual_board[row][self.col]):
                                break
                            else:
                                array_move.append((row,self.col))
                                break
        else:
            for col in range(start,end,step):
                if isinstance(board.virtual_board[self.row][col],int):
                    array_move.append((self.row,col))
                else:
                    if col != self.col:
                        if isinstance(board.virtual_board[self.row][col],Piece):
                            if board.is_ally_piece(self,board.virtual_board[self.row][col]):
                                break
                            else:
                                array_move.append((self.row,col))
                                break
        return array_move
