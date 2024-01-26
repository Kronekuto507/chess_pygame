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
        self.is_checked = False
        self.queen_side_pos = self.col - 2
        self.king_side_pos = self.col + 2

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

        if not self.has_moved:
            king_side_pos = self.col + 2
            queen_side_pos = self.col - 2
            rooks = self.get_rooks(board)
            if not rooks[1].has_moved and (isinstance(board.virtual_board[self.row][self.col + 1],int) and #AQUI HAY BUG
                isinstance(board.virtual_board[self.row][self.col + 2],int)):
                moves.append((self.row,king_side_pos))
            if not rooks[0].has_moved and (isinstance(board.virtual_board[self.row][self.col - 1],int) and
                isinstance(board.virtual_board[self.row][self.col - 2],int) and
                isinstance(board.virtual_board[self.row][self.col - 3], int)):
                moves.append((self.row,queen_side_pos))
        
        valid_moves = self.get_valid_moves(moves,board.get_enemy_pieces())
        return valid_moves
    
    def get_rooks(self,board):
        rook_array = []
        for col in range(0,COLS):
            if isinstance(board.virtual_board[self.row][col],Rook):
                rook_array.append(board.virtual_board[self.row][col])
        return rook_array
    
    def get_valid_moves(self,moves,enemy_pieces): #HAY UN BUG CON EL PEON
        valid_moves = moves
        for piece in enemy_pieces:
            for move in moves:
                for piece_move in piece.moves:
                    if move == piece_move and piece.color != self.color:
                        valid_moves.remove(move)
        return valid_moves

        
    
        

