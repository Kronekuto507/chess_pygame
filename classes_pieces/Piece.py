import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import *
import copy
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
    
    def is_legal_move(self,x,y,board):
        row,col = self.get_new_coordinates(x,y)
        #Almacenar tablero en una nueva variable para luego hacer los calculos de validación del movimiento
        board_copy = board.create_copy()
        board_copy.generate_moves()
        #Se iguala la pieza actual en el tablero a una nueva referencia
        piece_sample = board_copy.virtual_board[self.get_row()][self.get_column()]
        king = board_copy.get_king()
        enemy_pieces = board_copy.get_pieces()
        new_destination = (row,col)

        board_copy.print_board()
        #Mover pieza de forma virtual
        board_copy.update_board_status(row = self.get_row(),column = self.get_column(),new_column = new_destination[1],new_row = new_destination[0],piece = piece_sample)
        print("ESPACIO \n \n")

        board_copy.print_board()
        is_in_check = board_copy.is_in_check(king,enemy_pieces)

        print("ESPACIO TABLERO ORIGINAL \n \n")

        board.print_board()

        if not board.checked_status:
            if is_in_check and (new_destination in self.moves):
                return False
            if new_destination in self.moves:
               return True
        else:
            for piece in enemy_pieces:
                for move in piece.moves:
                    if new_destination == move:
                        board.checked_status = False
                        return True
            
        return False

    def move_piece(self, x, y,board):
        
        if self.is_legal_move(x,y,board):
            new_x,new_y = self.get_new_coordinates(x,y) 
            for move in self.moves:
                if new_x == move[0] and new_y == move[1]:
                    self.row = new_x
                    self.col = new_y
            if self.name == 'king':
                if (self.col == self.king_side_pos or self.col == self.queen_side_pos) and not self.has_moved and board.checked_status == False:
                    board.castle(self)
                    self.has_moved = True
                self.has_moved = True

            if self.name == 'rook':
                self.has_moved = True
            
            if self.name == 'pawn' and self.promo_rank == self.row:
                self.promoted = True
            board.current_player_color = 'black' if board.current_player_color == 'white' else 'white'
            self.calc_pos()
        else:
            print("Try again")
            
                    
                    


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



