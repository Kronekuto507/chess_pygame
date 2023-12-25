import pygame
from pygame.locals import *
from pathlib import Path

class Pawn(pygame.sprite.Sprite):
    def __init__(self, color, surface, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image= surface
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.set_image()

    def set_image(self):
        
        if self.color == "white":
            image = pygame.image.load(Path(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images\white_pawn.png")).convert_alpha()
              
        elif self.color == "black":
            image = pygame.image.load(Path(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images\black_pawn.png")).convert_alpha()
            
        self.image.blit(image,(0,0))
            
        
       
        
    
