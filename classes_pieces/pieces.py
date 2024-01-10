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
    
    def get_position(self):
        return (self.get_row(),self.get_column())
    
    '''def move_piece(self, x, y):
        piece_move_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\move-self.mp3")
        if self.is_selected:
            self.row,self.col = self.get_new_coordinates(x,y)
            self.calc_pos()
            piece_move_sound.play()'''

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
                
    def selection_status(self):
        return self.is_selected
    
    def generate_moves(self,board):
        
        moves = []

        for row in ROWS:
            for col in COLS:
                if self.selection_status():
                    if isinstance(int,board.virtual_board[row][col]):
                        moves.append((row,col))
                    else:
                        if board.is_ally_piece(self,board.virtual_board[row][col]):
                            break
                        else:
                            moves.append((row+1,col+1))
                            break
        return moves





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

class Queen(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'queen'

class Rook(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'rook'
        self.is_moved  = False
    
    def show_squares(self):
        if self.is_selected:
            for i in range(ROWS):
                if self.color == 'black':
                    pygame.draw.circle(self.surface,DIM_GREY,(self.pos_x*i + SIZE/2,self.pos_y + SIZE*i - SIZE + SIZE/2),25)
                elif self.color == "white":
                    pygame.draw.circle(self.surface,DIM_GREY,(self.pos_x + SIZE/2,self.pos_y - SIZE*i + SIZE - SIZE/2),25)
                

class Knight(Piece):
    def __init__(self, color, surface, row, col):
        super().__init__(color, surface, row, col)
        self.name = 'knight'

class King(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color, surface, row, col)
        self.name = 'king'
        self.is_moved = False

class Bishop(Piece):
    def __init__(self,color,surface,row,col):
        super().__init__(color,surface,row,col)
        self.name = 'bishop'

    def show_squares(self):
        pass
        

    

    

            
        
       
        
    
