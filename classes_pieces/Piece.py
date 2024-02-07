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
        self.true_moves = []
        
    
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
    
    def deselect(self):
        self.is_selected = False
    
    def get_row(self):
        return self.row
    
    def get_column(self):
        return self.col
    
    def get_starting_square_coordinates(self):
        return (self.get_row(),self.get_column())
    
    def is_legal_move(self,x,y,board):
        old_row = self.get_row()
        old_column = self.get_column()
        row,col = self.get_new_coordinates(x,y)
        #Almacenar tablero en una nueva variable para luego hacer los calculos de validación del movimiento
        board_copy = board.create_copy()
        board_copy.generate_moves()
        moves = self.moves
        #Se iguala la pieza actual en el tablero a una nueva referencia
        piece_sample = board_copy.virtual_board[self.get_row()][self.get_column()]
        new_destination = (row,col)

        board_copy.print_board()
        #Mover pieza de forma virtual
        board_copy.update_board_status(row = self.get_row(),column = self.get_column(),new_column = col,new_row = row,piece = piece_sample)
        print("board_copy board")
        board_copy.print_board()
        king = board.get_king()
        is_in_check = board_copy.validate_if_check_after_move(king)

        def detect_if_false(board,old_column,old_row):
            board.virtual_board[old_row][old_column] = self
            self.row = old_row
            self.col = old_column
            self.true_moves = moves

        if not board.checked_status:

            if is_in_check and new_destination in moves:
                detect_if_false(board,old_column,old_row)
                return False
            
            if new_destination in moves:
               self.true_moves= moves
               square = board.virtual_board[new_destination[0]][new_destination[1]]
               if isinstance(square,Piece) and board.is_ally_piece(self,square):
                   detect_if_false(board,old_column,old_row)
                   return False
               
               return True
               
        else:

            if not is_in_check and new_destination in moves:
                board.checked_status = False
                self.true_moves = moves
        
                if isinstance(square,Piece) and board.is_ally_piece(self,square):
                   detect_if_false(board,old_column,old_row)
                   return False
                
                return True
            
            elif is_in_check and new_destination in moves:
                detect_if_false(board,old_column,old_row)
                return False
        return False

    def move_piece(self, x, y,old_column,old_row,board):
        piece_move_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\move-self.mp3")
        if self.is_legal_move(x,y,board):
            new_x,new_y = self.get_new_coordinates(x,y) 
            for move in self.true_moves:
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
            
            if self.name == 'pawn':
                self.has_moved = True
                if self.promo_rank == self.row:
                    self.promoted = True

            board.moved_piece = self
            self.deselect()
            self.calc_pos()
            if board.moved_piece.name == 'pawn' and board.moved_piece.has_promoted():
                board.promote(self.moved_piece,old_row,old_column)

            elif board.moved_piece.name in ('pawn','rook','queen','king','knight','bishop'):
                board.update_board_status(old_row,old_column,board.moved_piece.get_column(),board.moved_piece.get_row(),board.moved_piece)
            piece_move_sound.play()
            board.current_player_color = 'black' if board.current_player_color == 'white' else 'white'

            board.generate_moves()

            #Comprobar si está en jaque el rey luego de haber movido
            king = board.get_king()
            enemy_pieces = board.get_pieces()
            ally_pieces = board.get_pieces(get_ally_pieces = True)
            ally_moves = board.get_moves(ally_pieces
                                         )
            valid_moves_king = board.get_valid_moves_king(king,enemy_pieces)
            board.virtual_board[king.get_row()][king.get_column()].assign_moves(valid_moves_king)
            is_check,enemy_moves = board.is_in_check(king,enemy_pieces)
            board.checkmate = board.is_checkmate(king,enemy_moves,ally_moves)
        else:
            self.deselect()
            board.generate_moves()
            
                    
    def show_squares(self,board):

        transparent_surface = pygame.Surface((SIZE,SIZE),pygame.SRCALPHA)
        alpha_value = 100
        green_with_alpha = TRANSPARENT_GREEN + (alpha_value,)

        showable_moves = self.moves
        for row in board.virtual_board:
            for column in row:
                if isinstance(column,Piece) and board.is_ally_piece(self,column):
                    for move in self.moves:
                        if move[0] == column.get_row() and move[1] == column.get_column():
                            showable_moves.remove(move)


        transparent_surface.fill(green_with_alpha)
        for move in showable_moves:
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



