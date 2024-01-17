import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from classes_pieces.Bishop import Bishop
from classes_pieces.Rook import Rook
from classes_pieces.King import King

class Queen(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'queen'
        self.rook_instance = Rook(color,surface,row,col)
        self.bishop_instance = Bishop(color,surface,row,col)
        self.king_instance = King(color,surface,row,col)
        '''Chequear todo eso de arriba después'''
    def generate_moves(self,board):
        moves = []
        moves.extend(self.rook_instance.generate_moves(board))
        moves.extend(self.bishop_instance.generate_moves(board))
        moves.extend(self.king_instance.generate_moves(board))
        return moves