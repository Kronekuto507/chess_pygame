import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import *
import math
class Piece:
    def __init__(self, color, surface,row,col):
        self.surface= surface
        self.image = None
        self.color = color
        self.row = row
        self.col = col
        self.pos_x = 0
        self.pos_y = 0
        self.name = ''
        self.is_selected = False
        self.moves = []
        self.calc_pos()
        
    
    def calc_pos(self):
        self.pos_x = SIZE * self.col 
        self.pos_y = SIZE * self.row
    
    def create_image(self):

        file_name, suffix = f'{self.color}_{self.name}','.png'
        path = Path(r'c:\Users\aaron\Desktop\Programacion\Python\ajedrez\pieces_images',file_name).with_suffix(suffix)
        if self.color == "white":
            self.image = pygame.image.load(path).convert_alpha()     
        elif self.color == "black":
            self.image = pygame.image.load(path).convert_alpha()

    def set_image(self):

        self.surface.blit(self.image,(self.pos_x,self.pos_y))
    
    def select_piece(self,mouse_x,mouse_y):
        
        calc_x,calc_y = mouse_x >= self.pos_x and mouse_x <= self.pos_x + SIZE, mouse_y >= self.pos_y and mouse_y <= self.pos_y + SIZE
        if calc_x and calc_y:
            self.is_selected = True
            print(f'{calc_x,},{calc_y} ')
            print(f"{self.name}")
    
    def deselect(self):
        self.is_selected = False
    
    def get_row(self):
        return self.row
    
    def get_column(self):
        return self.col
    
    def get_starting_square_coordinates(self):
        return (self.get_row(),self.get_column())
    
    def move_piece(self, x, y,board):
        
        if self.is_selected:
            new_x,new_y = self.get_new_coordinates(x,y) 
            for move in self.moves:
                if new_x == move[0] and new_y == move[1]:
                    self.row = new_x
                    self.col = new_y
                    if self.name == 'king':
                        self.has_moved = True
                        if self.col == self.king_side_pos or self.col == self.queen_side_pos:
                            board.castle(self)
                    if self.name == 'rook':
                        self.has_moved = True
                    self.calc_pos()
                    break


    def show_squares(self):

        transparent_surface = pygame.Surface((SIZE,SIZE),pygame.SRCALPHA)
        alpha_value = 100
        green_with_alpha = TRANSPARENT_GREEN + (alpha_value,)

        transparent_surface.fill(green_with_alpha)
        for move in self.moves:
            coord_x,coord_y = SIZE*move[1],SIZE*move[0]
            self.surface.blit(transparent_surface,(coord_x,coord_y))
        

    def get_new_coordinates(self,x,y):
        this_row = 0
        this_col = 0
        for i in range (ROWS):
            this_col = SIZE * i
            for j in range(COLS):
                this_row = SIZE * j
                if (x >= this_row and x <= this_row + SIZE) and (y>= this_col and y<=this_col + SIZE):
                    return i,j
                
    def selection_status(self):
        return self.is_selected
    
    def assign_moves(self,moves):
        self.moves = moves


