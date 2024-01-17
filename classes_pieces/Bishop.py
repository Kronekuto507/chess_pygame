import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from board.constants import *

class Bishop(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color,surface,row,col)
        self.name = 'bishop'

    def generate_moves(self, board):

        moves = []
        south_east = self.calc_bishop_moves(start_row=self.row,end_row=ROWS,start_col=self.col,end_col=COLS,step_row=1,step_col=1,board=board)
        north_east = self.calc_bishop_moves(start_row=self.row,end_row=-1,start_col=self.col,end_col=COLS,step_row=-1,step_col=1,board=board)
        north_west = self.calc_bishop_moves(start_row=self.row,end_row=-1,start_col=self.col,end_col=-1,step_row=-1,step_col=-1,board=board)
        south_west = self.calc_bishop_moves(start_row=self.row,end_row=ROWS,start_col=self.col,end_col=-1,step_row=1,step_col=-1,board=board)
        moves = north_east + north_west + south_east + south_west
        return moves
    
    def calc_bishop_moves(self,start_row,end_row,start_col,end_col,step_row,step_col,board):
        array_moves = []
        array_counter = 0
        previous_col - self.row
        previous_col = self.col
        for row in range(start_row,end_row,step_row):
            for col in range(start_col,end_col,step_col):
                if row != self.row:
                    diff_row = previous_row - row
                    diff_col = previous_col - col
                    if isinstance(board[row][col],int):
                        if abs(diff_col) == abs(diff_row):
                            array_counter.append((row,col))
                            previous_row = array_moves[array_counter][0]
                            previous_col = array_moves[array_counter][1]
                            array_counter += 1
        return array_moves