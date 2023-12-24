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
        self.draw_board()
    
    def draw_cell(self,x,y, color):
        pygame.draw.rect(self.drawn_board, color, Rect(x,y,self.SIZE,self.SIZE))

    def draw_board(self):
        
        for i in range(0,self.ROWS):

            for j in range(0,self.COLS):

                if i%2==0:
                    if j%2==0:
                        self.draw_cell(self.SIZE*j//2,self.SIZE*i//2, self.starter_color)
                    else:
                        self.draw_cell(self.SIZE*j//2,self.SIZE*i//2,self.next_color)
                else:
                    if j%2==0:
                        self.draw_cell(self.SIZE*j//2,self.SIZE*i//2, self.next_color)
                    else:
                        self.draw_cell(self.SIZE*j//2,self.SIZE*i//2,self.starter_color)
                        
    def render_board(self,screen,width,height):
        screen.blit(self.drawn_board, (width/2 - 250,height/2 - 250))





            
            
                