import pygame
from pygame.locals import *
from classes_pieces.pieces import Pawn
from .constants import CREMA,VERDE,ROWS,COLS,SIZE,WIDTH,HEIGHT

class Board:
    def __init__(self):
        
        self.drawn_board = pygame.Surface((WIDTH,HEIGHT))#Plantilla en donde se dibujara el resto de cuadros
        
        self.surf_cord = {} #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        self.draw_board()
        
    def dictionary_surfaces_coordinates(self, surface, coordinates, row, col):
        surf_cord = {
            "surf_" + str(row) + str(col): surface,
            "coordinate_" + str(row) + str(col): coordinates
        }
        return surf_cord
    
    def create_surface(self,color):
        rectangle_surface = pygame.surface.Surface((SIZE,SIZE))
        rectangle_surface.fill(color=color)
        return rectangle_surface

    def draw_board(self):
        
        for row in range(0,ROWS):
            self.virtual_board.append([])
            for col in range(0,COLS):
                coord_x,coord_y = SIZE*col//2,SIZE*row//2
            
                if row%2==0:
                    if col%2==0:    
                        surface = self.create_surface(CREMA)    
                    else:   
                        surface = self.create_surface(VERDE)    
                else:
                    if col%2==0:
                        surface = self.create_surface(VERDE)
                  
                    else:
                        surface = self.create_surface(CREMA)

                self.drawn_board.blit(surface,Rect(coord_x,coord_y,SIZE,SIZE))
                        
                
                if row == 0:
                    self.virtual_board[row].append(Pawn('black',self.drawn_board,row,col))
                elif row == 3:
                    self.virtual_board[row].append(Pawn('white',self.drawn_board,row,col))
                else:
                    self.virtual_board[row].append(0)
                    


                        
    def render_board(self,screen,width,height):
        screen.blit(self.drawn_board, (0,0))
        for row in range(0,ROWS):
            for col in range(0,COLS):
                if isinstance(self.virtual_board[row][col], Pawn):
                    self.virtual_board[row][col].set_image()
        print(self.virtual_board)





            
            
                