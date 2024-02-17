import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from board.constants import *

class Pawn(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'pawn'
        self.has_moved = False
        self.promo_rank = 0 if self.color == 'white' else 7
        self.promoted = False
        self.attacking_squares = []
    def generate_moves(self,board):
        moves = []
        step = 1 if self.color == "black" else -1
        offsett_capture = [(step,1),(step,-1)]
        new_row = self.row + step
        next_row = self.row
        if new_row <= 7 and new_row >= 0:
            if self.has_moved:
                next_row  += step
                if isinstance(board.virtual_board[next_row][self.col],int):
                    moves.append((next_row,self.col))
            else:
                    next_row += step
                    if isinstance(board.virtual_board[next_row][self.col],int):
                        moves.append((next_row, self.col))
                        if not isinstance(board.virtual_board[new_row][self.col],Piece):
                            if isinstance(board.virtual_board[next_row + step][self.col],int):
                                moves.append((next_row + step, self.col))

            for element in offsett_capture:
                row = self.row + element[0]
                col = self.col + element[1]
                if row >= 0 and row <= 7 and col>=0 and col <= 7:
                    if isinstance(board.virtual_board[row][col],Piece) and not board.is_ally_piece(self,board.virtual_board[row][col]):
                        moves.append((row,col))
                    self.attacking_squares.append((row,col))

        return moves
    
    def has_promoted(self):
        return self.promoted
    
    def clone(self):
        new_pawn = Pawn(self.color,self.surface,self.row,self.col)
        new_pawn.has_moved = self.has_moved
        new_pawn.promoted = self.promoted
        new_pawn.attacking_squares = self.attacking_squares
        return new_pawn

                
