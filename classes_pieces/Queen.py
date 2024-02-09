
from pygame.locals import *
from classes_pieces.Piece import Piece
from classes_pieces.Bishop import Bishop
from classes_pieces.Rook import Rook


class Queen(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'queen'
        
    def generate_moves(self,board):
        moves = []
        rook_instance = Rook(self.color,self.surface,self.row,self.col)
        bishop_instance = Bishop(self.color,self.surface,self.row,self.col)
        moves.extend(rook_instance.generate_moves(board))
        moves.extend(bishop_instance.generate_moves(board))
        return moves
    
    def clone(self):
        return Queen(self.color,self.surface,self.row,self.col)