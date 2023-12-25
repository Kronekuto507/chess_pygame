import pygame
from pygame.locals import *


WIDTH = 1000
class Board:
    def __init__(self):
        
        self.drawn_board = pygame.Surface((500,500))
        self.ROWS,self.COLS = 8,8
        self.SIZE = WIDTH/self.COLS
        self.next_color = pygame.Color(18,95,74) #Verde
        self.starter_color = pygame.Color(250, 233, 169) #Crema
        self.surf_cord = {}
        self.draw_board()
        
    def dictionary_surfaces_coordinates(self, surface, coordinates, row, col):
        surf_cord = {
            "surf_" + str(row) + str(col): surface,
            "coordinate_" + str(row) + str(col): coordinates
        }
        return surf_cord
    
    def create_surface(self,color):
        rectangle_surface = pygame.surface.Surface((self.SIZE,self.SIZE))
        rectangle_surface.fill(color=color)
        return rectangle_surface
    
    def draw_cell(self,x,y,color):
        rectangle_surface = self.create_surface(color)
        self.drawn_board.blit(rectangle_surface,Rect(x,y,self.SIZE,self.SIZE))

    def draw_board(self):
        
        for i in range(0,self.ROWS):
            dictionary = None
            for j in range(0,self.COLS):
                coord_x,coord_y = self.SIZE*j//2,self.SIZE*i//2
            
                if i%2==0:
                    if j%2==0:
                        self.draw_cell(coord_x,coord_y, self.starter_color)
                        surface = self.create_surface(self.starter_color)
                        dictionary = self.dictionary_surfaces_coordinates(surface,(coord_x,coord_y),i,j)
                    else:
                        self.draw_cell(coord_x,coord_y,self.next_color)
                        surface = self.create_surface(self.next_color)
                        dictionary = self.dictionary_surfaces_coordinates(surface,(coord_x,coord_y),i,j)
                    
                else:
                    if j%2==0:
                        self.draw_cell(coord_x,coord_y, self.next_color)
                        surface = self.create_surface(self.next_color)
                        dictionary = self.dictionary_surfaces_coordinates(surface,(coord_x,coord_y),i,j)
                        
                    else:
                        self.draw_cell(coord_x,coord_y,self.starter_color)
                        surface = self.create_surface(self.starter_color)
                        dictionary = self.dictionary_surfaces_coordinates(surface,(coord_x,coord_y),i,j)
                self.surf_cord.update(dictionary)
                self.drawn_board.blit(self.surf_cord["surf_" + str(i) + str(j)],(self.surf_cord["coordinate_" + str(i) + str(j)][0],self.surf_cord["coordinate_" + str(i) + str(j)][1]))


                        
    def render_board(self,screen,width,height):
        screen.blit(self.drawn_board, (width/2 - 250,height/2 - 250))





            
            
                