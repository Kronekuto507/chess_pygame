import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from classes_pieces.Bishop import Bishop
from classes_pieces.King import King
from classes_pieces.Queen import Queen
from classes_pieces.Knight import Knight
from classes_pieces.Rook import Rook
from classes_pieces.Pawn import Pawn
from .constants import VERDE,ROWS,COLS,SIZE


class Board:
    
    def __init__(self, screen):
        #Plantilla en donde se dibujara el resto de cuadros
        #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        self.selected_piece = None
        self.screen = screen
        b_starter_row = 0
        self.b_array = [Rook('black',screen,b_starter_row,0),Knight('black',screen,b_starter_row,1)
                   ,Bishop('black',screen,b_starter_row,2),Queen('black',screen,b_starter_row,3),King('black',screen,b_starter_row,4)
                    ,Bishop('black',screen,b_starter_row,5),Knight('black',screen,b_starter_row,6),Rook('black',screen,b_starter_row,7)]
        w_starter_row = 7
        self.w_array = [Rook('white',screen,w_starter_row,0),Knight('white',screen,w_starter_row,1)
                   ,Bishop('white',screen,w_starter_row,2),Queen('white',screen,w_starter_row,3),King('white',screen,w_starter_row,4)
                    ,Bishop('white',screen,w_starter_row,5),Knight('white',screen,w_starter_row,6),Rook('white',screen,w_starter_row,7)]

    
    def draw_cell(self,surface,color,x,y):
        pygame.draw.rect(surface,color,(x,y,SIZE,SIZE))

    def draw_board(self):
        
        for row in range(0,ROWS):
            for col in range(row%2,ROWS,2):
                coord_y,coord_x = SIZE*col,SIZE*row
                self.draw_cell(self.screen,VERDE,coord_x,coord_y)

        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece):
                    piece.set_image()
        
              
    def create_virtual_board(self):
        
        for row in range(ROWS):
            self.virtual_board.append([])
            for col in range(COLS):
                    if row == 6:
                        w_pawn = Pawn('white',self.screen,row,col)
                        self.virtual_board[row].append(w_pawn)
                        self.virtual_board[row][col].create_image()  
                    elif row == 1:
                        b_pawn = Pawn('black', self.screen,row,col)
                        self.virtual_board[row].append(b_pawn)
                        self.virtual_board[row][col].create_image()
        
        for col in range (COLS):
            self.virtual_board[0].append(self.b_array[col])
            self.virtual_board[7].append(self.w_array[col])
            if isinstance(self.virtual_board[0][col],Piece):
                self.virtual_board[0][col].create_image()
            if isinstance(self.virtual_board[7][col],Piece):
                self.virtual_board[7][col].create_image()
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.virtual_board[row] is not Piece and (row != 0 and row != 7 and row != 1 and row != 6): #Para dejar el polimorfismo alli
                    self.virtual_board[row].append(0)
    
    def is_in_check(self):
        pass

    def is_checkmate(self):
        pass


    def generate_pieces_moves(self, piece_arg):
        if piece_arg is (Rook,Knight,Bishop,Queen,King,Pawn) and hasattr(piece_arg,"generate_moves"):
            return piece_arg.generate_moves(self.virtual_board)
        
    def is_ally_piece(self,main_piece,other_piece):
        return True if main_piece.color == other_piece.color else False
                
    
    def select_piece_on_board(self,x,y):
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece):
                    if self.selected_piece is None: #Se detecta si no existe ya un objeto seleccionado, de ser el caso, seleccionar directamente
                        piece.select_piece(x,y)
                        self.selected_piece = piece
                    else: #Si ya hay un objeto, este 
                        selected_row = piece.get_row()
                        selected_col = piece.get_column()
                        self.virtual_board[selected_row][selected_col].deselect()
                        piece.select_piece(x,y)
                        self.selected_piece = piece

    def move_piece_on_board(self,x,y):
        piece_capture_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\capture.mp3")
        old_column = 0
        old_row = 0
        moved_piece = None
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece):
                    if piece.is_selected:
                        old_column = piece.get_column()
                        old_row = piece.get_row()
                        piece.move_piece(x,y)
                        if piece.name == 'pawn':
                            piece.has_moved = True
                        moved_piece = piece
                        piece.deselect()
        for row in self.virtual_board:
            print(row)
        self.update_board_status(old_row,old_column,moved_piece.get_column(),moved_piece.get_row(),moved_piece)
        self.generate_moves()
        for row in self.virtual_board:
            print(row)
                     
        
    def generate_moves(self):
        for row in self.virtual_board:
            for element in row:
                valid_types = (Rook,Knight,Bishop,Queen,King,Pawn)
                if isinstance(element,valid_types)  and hasattr(element,"generate_moves"):
                    moves = element.generate_moves(self)
                    element.assign_moves(moves)
                    print(element.moves)

    def update_board_status(self,row,column,new_column,new_row,piece):
        self.virtual_board[row][column] = 0
        self.virtual_board[new_row][new_column] = piece


                            
            












            
            
                