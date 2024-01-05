import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import SIZE,DIM_GREY,ROWS,COLS

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
    
    def move_piece(self,x,y):
        pass

    def show_squares(self):
        pass

    def get_new_coordinates(self,x,y):
        this_row = 0
        this_col = 0
        for i in range (ROWS):
            this_col = SIZE * i
            for j in range(COLS):
                this_row = SIZE * j
                if (x >= this_row and x <= this_row + SIZE) and (y>= this_col and y<=this_col + SIZE):
                    return i,j




class Pawn(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'pawn'

    def show_squares(self):
        starter_steps = 3
        #Se dibuja unos circulos en el tablero que representan los cuadros en los que la pieza se puede mover
        if self.is_selected:
            for column in range(1,starter_steps):
                if self.color == 'black':
                    pygame.draw.circle(surface=self.surface,color=DIM_GREY,center=(self.pos_x + SIZE/2,self.pos_y*column + SIZE + SIZE/2),radius=25)
                elif self.color == 'white':
                    pygame.draw.circle(surface=self.surface,color=DIM_GREY,center=(self.pos_x + SIZE/2,self.pos_y - SIZE * column + SIZE - SIZE/2),radius=25)
    
    def move_piece(self, x, y):
        if self.is_selected:
            new_row,new_col = self.get_new_coordinates(x,y)
            self.pos_x = SIZE * new_col
            self.pos_y = SIZE * new_row          

class Queen(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'queen'

class Rook(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'rook'
    
    def show_squares(self):
        return super().show_squares()

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

    def show_squares(self):
        pass
        

    

    

            
        
       
        
    
