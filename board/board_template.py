import pygame
from pygame.locals import *
from classes_pieces.pieces import Pawn
from .constants import CREMA,VERDE,ROWS,COLS,SIZE,WIDTH,HEIGHT

class Board:
    def __init__(self):
        #Plantilla en donde se dibujara el resto de cuadros
        self.surf_cord = {} #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        
    def dictionary_surfaces_coordinates(self, surface, coordinates, row, col):
        surf_cord = {
            "surf_" + str(row) + str(col): surface,
            "coordinate_" + str(row) + str(col): coordinates
        }
        return surf_cord
    
    def draw_cell(self,surface,color,x,y):
        pygame.draw.rect(surface,color,(x,y,SIZE,SIZE))

    def draw_board(self,screen):
        
        for row in range(0,ROWS):
            self.virtual_board.append([])
            for col in range(0,COLS):
                coord_y,coord_x = SIZE*col,SIZE*row
                   
                    
                        
    def render_board(self,screen):
        self.draw_board(screen=screen)
        print(self.virtual_board)





            
            
                