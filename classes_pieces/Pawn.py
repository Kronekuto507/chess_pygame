import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'pawn'
        self.has_moved = False
    
    def generate_moves(self,board):
        moves = []
        step = 1 if self.color == "black" else -1
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
                    if isinstance(board.virtual_board[next_row + step][self.col],int):
                        moves.append((next_row + step, self.col))
        return moves

                
