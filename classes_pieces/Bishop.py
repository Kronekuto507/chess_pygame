import pygame
from pygame.locals import *
from classes_pieces.pieces import Piece
from board.constants import *

class Bishop(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color,surface,row,col)
        self.name = 'bishop'

    def generate_moves(self, board):

        moves = []
        south_east = []
        previous_row = self.row
        previous_col = self.col
        #Code for adding the southeast possible moves for the piece
        south_east_counter = 0
        for row in range(self.row,ROWS):
            for col in range(self.col,COLS):
                if row != self.row:
                    diff_row = previous_row - row
                    diff_col = previous_col - col
                    if isinstance(board[row][col], int):
                        if abs(diff_col) == abs(diff_row):
                            south_east.append((row,col))
                            previous_row = south_east[south_east_counter][0]
                            previous_col = south_east_counter[south_east_counter][1]
                            south_east_counter += 1
                            #Updates the 


        north_east = []
        #Code for adding the north eastern possible moves for the bishop
        previous_row = self.row
        previous_col = self.col
        north_east_counter = 0
        for row in range(self.row,-1,-1):
            for col in range(self.col,COLS):
                if row != self.row:
                    diff_row = previous_row - row
                    diff_col = previous_col - col
                    if isinstance(board[row][col], int):
                        if abs(diff_col) == abs(diff_row):
                            north_east.append((row,col))
                            previous_row = north_east[north_east_counter][0]
                            previous_col = north_east_counter[north_east_counter][1]
                            north_east_counter += 1
        
        north_west = []
        #Code for adding the north western possible moves for the bishop
        previous_row = self.row
        previous_col = self.col
        north_west_counter = 0
        for row in range(self.row, -1,-1):
            for col in range(self.col,-1,-1):
                if row != self.row:
                    diff_row = previous_row - row
                    diff_col = previous_col - col
                    if isinstance(board[row][col],int):
                        if abs(diff_col) == abs(diff_row):
                            north_west.append((row,col))
                            previous_row = north_west[north_west_counter][0]
                            previous_col = north_west[north_west_counter][1]
                            north_west_counter += 1
        
        south_west = []
        previous_row = self.row
        previous_col = self.col
        south_west_counter = 0
        for row in range(self.row,ROWS):
            for col in range(self.col,-1,-1):
                if row != self.row:
                    diff_row = previous_row - row
                    diff_col = previous_col - col
                    if isinstance(board[row][col],int):
                        if abs(diff_col) == abs(diff_row):
                            south_west.append((row,col))
                            previous_row = south_west[south_west_counter][0]
                            previous_col = south_west[south_west_counter][1]
                            south_east_counter += 1

        moves = north_east + north_west + south_east + south_west
        return moves

    def show_squares(self):
        pass