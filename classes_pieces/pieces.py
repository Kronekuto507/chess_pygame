import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import SIZE

class Piece:
    def __init__(self, color, surface,row,col):
        self.image= surface
        self.color = color
        self.row = row
        self.col = col
        self.pos_x = 0
        self.pos_y = 0
        self.name = ''
        self.is_selected = False
        
        
    
    def calc_pos(self):
        self.pos_x = SIZE * self.col 
        self.pos_y = SIZE * self.row
    
    def set_image(self):
        file_name, suffix = f'{self.color}_{self.name}','.png'
        self.calc_pos()
        path = Path(r'c:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images',file_name).with_suffix(suffix)
        if self.color == "white":
            image = pygame.image.load(path).convert_alpha()
            
              
        elif self.color == "black":
            image = pygame.image.load(path).convert_alpha()
        
        self.image.blit(image,(self.pos_x,self.pos_y))
    
    def select_piece(self,mouse_x,mouse_y):
        self.calc_pos()
        calc_x,calc_y = mouse_x >= self.pos_x and mouse_x <= self.pos_x + SIZE, mouse_y >= self.pos_y and mouse_y <= self.pos_y + SIZE
        if calc_x and calc_y:
            self.is_selected = True
            print(f'{calc_x,},{calc_y} ')
            print(f"{self.name}")


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

class King(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color, surface, row, col)
        self.name = 'king'

class Bishop(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color,surface,row,col)
        self.name = 'bishop'

    

    

            
        
       
        
    
