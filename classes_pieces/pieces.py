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
        self.calc_pos()
    
    def calc_pos(self):
        self.pos_x = SIZE * self.col + SIZE //2
        self.pos_y = SIZE * self.row + SIZE//2


class Pawn(Piece):

    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        
    
    def set_image(self):
        
        if self.color == "white":
            image = pygame.image.load(Path(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images\white_pawn.png")).convert_alpha()
              
        elif self.color == "black":
            image = pygame.image.load(Path(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images\black_pawn.png")).convert_alpha()
            
        self.image.blit(image,(self.pos_x,self.pos_y))
    

            
        
       
        
    
