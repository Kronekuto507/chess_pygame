import pygame
from pygame.locals import *
from classes_pieces.pieces import Pawn,Rook,Knight,Queen,Bishop,King, Piece
from .constants import CREMA,VERDE,ROWS,COLS,SIZE,WIDTH,HEIGHT

class Board:
    def __init__(self):
        #Plantilla en donde se dibujara el resto de cuadros
        #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        self.selected_piece = None
    
    def draw_cell(self,surface,color,x,y):
        pygame.draw.rect(surface,color,(x,y,SIZE,SIZE))

    def draw_board(self,screen):
        
        for row in range(0,ROWS):
            for col in range(row%2,ROWS,2):
                coord_y,coord_x = SIZE*col,SIZE*row
                self.draw_cell(screen,VERDE,coord_x,coord_y)

        b_starter_row = 0
        b_array = [Rook('black',screen,b_starter_row,0),Knight('black',screen,b_starter_row,1)
                   ,Bishop('black',screen,b_starter_row,2),Queen('black',screen,b_starter_row,3),King('black',screen,b_starter_row,4)
                    ,Bishop('black',screen,b_starter_row,5),Knight('black',screen,b_starter_row,6),Rook('black',screen,b_starter_row,7)]
        w_starter_row = 7
        w_array = [Rook('white',screen,w_starter_row,0),Knight('white',screen,w_starter_row,1)
                   ,Bishop('white',screen,w_starter_row,2),Queen('white',screen,w_starter_row,3),King('white',screen,w_starter_row,4)
                    ,Bishop('white',screen,w_starter_row,5),Knight('white',screen,w_starter_row,6),Rook('white',screen,w_starter_row,7)]
        
        for row in range(ROWS):
            b_array[row].set_image()
            w_array[row].set_image()
            self.virtual_board.append([])
            for col in range(COLS):
                    if row == 6:
                        w_pawn = Pawn('white',screen,row,col)
                        w_pawn.set_image()
                        self.virtual_board[row].append(w_pawn)
                    elif row == 1:
                        b_pawn = Pawn('black', screen,row,col)
                        b_pawn.set_image()
                        self.virtual_board[row].append(b_pawn)
        
    

        #Colocar piezas en el tablero
        for col in range (COLS):
            self.virtual_board[0].append(b_array[col])
            self.virtual_board[7].append(w_array[col])
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.virtual_board[row] is not Piece and (row != 0 and row != 7 and row != 1 and row != 6): #Para dejar el polimorfismo alli
                    self.virtual_board[row].append(0)
        
              
    def render_board(self,screen):
        self.draw_board(screen=screen)
        print(self.virtual_board)







            
            
                