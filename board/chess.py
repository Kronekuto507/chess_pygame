import pygame
from pygame.locals import *


WIDTH = 600
HEIGHT = 600 
class Board:
    def __init__(self, screen):
        
        self.ROWS,self.COLS = 8,8
        self.SIZE = WIDTH/self.COLS
        self.next_color = pygame.Color(18,95,74) #Verde
        self.starter_color = pygame.Color(250, 233, 169) #Crema
        self.screen = screen
    
    def draw_cell(self,x,y, color):
        pygame.draw.rect(self.screen, color, Rect(x,y,self.SIZE,self.SIZE))

    def draw_board(self):
        
        for i in range(0,self.ROWS):

            for j in range(0,self.COLS):

                if i%2==0:
                    if j%2==0:
                        self.draw_cell(self.SIZE*j,self.SIZE*i, self.starter_color)
                    else:
                        self.draw_cell(self.SIZE*j,self.SIZE*i,self.next_color)
                else:
                    if j%2==0:
                        self.draw_cell(self.SIZE*j,self.SIZE*i, self.next_color)
                    else:
                        self.draw_cell(self.SIZE*j,self.SIZE*i,self.starter_color)


            
            
                