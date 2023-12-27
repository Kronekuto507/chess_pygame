import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import SIZE
from os import path
class Piece:
    def __init__(self, color, surface,row,col):
        self.image= surface
        self.color = color
        self.row = row
        self.col = col
        self.pos_x = 0
        self.pos_y = 0
        self.name = ''
        
    
    def calc_pos(self):
        self.pos_x = SIZE * self.col 
        self.pos_y = SIZE * self.row
    
    def set_image(self):
        self.calc_pos()
        file_name, suffix = f'{self.color}_{self.name}','.png'

        path = Path(r'c:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images',file_name).with_suffix(suffix)
        if self.color == "white":
            image = pygame.image.load(path).convert_alpha()
            
              
        elif self.color == "black":
            image = pygame.image.load(path).convert_alpha()
        
        self.image.blit(image,(self.pos_x,self.pos_y))
       


class Pawn(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'pawn'

class Queen(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'queen'

class Rook(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'rook'

class Knight(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'knight'

    

    

            
        
       
        
    
