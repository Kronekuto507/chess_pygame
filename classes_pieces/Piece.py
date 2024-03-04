import pygame
from pygame.locals import *
from pathlib import Path
from board.constants import *
import math
import time
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
        self.did_legal_move = False

        self.old_positions = None
        self.goal_positions = None
        
    
    def calc_pos(self):
        self.pos_x = SIZE * self.col 
        self.pos_y = SIZE * self.row
    
    def animate(self):
        new_pos_x = SIZE * self.col
        new_pos_y = SIZE * self.row

        dx = round((abs(self.pos_x - new_pos_x))/((self.col + 1)))
        dy = round((abs(self.pos_y - new_pos_y))/((self.row + 1)))

        if self.name in ('queen', 'bishop','pawn'):
            dx = dy

        velocity_x = dx if new_pos_x > self.pos_x else (-dx if new_pos_x < self.pos_x else 0)
        velocity_y = dy if new_pos_y > self.pos_y else (-dy if new_pos_y < self.pos_y else 0)
        
        if new_pos_x != self.pos_x: 
            self.pos_x += velocity_x
        if new_pos_y != self.pos_y:
            self.pos_y += velocity_y
        
        if dx == 0 and dy == 0:
            self.pos_x = new_pos_x
            self.pos_y = new_pos_y
    
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
    
    def get_coordinates_x_y(self):
        return self.pos_x,self.pos_y

    
    def is_legal_move(self,x,y,board):
        old_row = self.get_row()
        old_column = self.get_column()
        row,col = self.get_new_coordinates(x,y)
        #Almacenar tablero en una nueva variable para luego hacer los calculos de validación del movimiento
        board_copy = board.create_copy()
        board_copy.generate_moves()

        print("\n \n")
        print("Copia del objeto board: variable board_copy en el metodo is_legal_move antes de llamar el metodo update_board_status de la variable board_capy")
        board_copy.print_board()
        print("\n \n")

        moves = self.moves
        #Se iguala la pieza actual en el tablero a una nueva referencia

        piece_sample = board_copy.virtual_board[self.get_row()][self.get_column()]


        new_destination = (row,col)
        #Mover pieza de forma virtual
        board_copy.update_board_status(row = self.get_row(),column = self.get_column(),new_column = col,new_row = row,piece = piece_sample)
        
        print("\n \n")
        print("Copia del objeto board: variable board_copy en el metodo is_legal_move despues de llamar el metodo update_board_status de la variable board_capy")
        board_copy.print_board()
        print("\n \n")

        king = board.get_king()
        is_in_check = board_copy.validate_if_check_after_move(king)

        def detect_if_false(board,old_column,old_row):
            board.virtual_board[old_row][old_column] = self
            self.row = old_row
            self.col = old_column
            self.true_moves = moves

        if not board.checked_status:
            if self.name == 'pawn':
                self.row = old_row
                self.col = old_column
                if board.check_if_en_passant() and self.show_en_passant != None and not self.has_done_en_passant:
                    if new_destination == self.show_en_passant:
                        self.true_moves = moves
                        self.has_done_en_passant = True
                        return True
                    
            if self.name == 'king':
                self.row = old_row
                self.col = old_column
                position = (row,col)
                rooks = board.get_rooks_for_castling(self)
                main_board_enemy_pieces = board.get_pieces()
                castling_condition_array = []
                if int(len(rooks)) > 0:
                    for rook in rooks:
                        print("Impresion del tablero en el metodo is_legal_move dentro del condicional para detectar si el rey puede enrocar")
                        board.print_board()
                        castling_condition_array.append(board.check_if_castle(self,rook,main_board_enemy_pieces))
                
                castling_condition_array = [x for x in castling_condition_array if x]
                castling_squares = list(self.castling_squares.values())

                for condition in castling_condition_array:
                    if position in castling_squares and condition:
                        self.can_castle_array = castling_condition_array
                        return True


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
                square = board.virtual_board[new_destination[0]][new_destination[1]]
                if isinstance(square,Piece) and board.is_ally_piece(self,square):
                   detect_if_false(board,old_column,old_row)
                   return False
                
                return True
            
            elif is_in_check and new_destination in moves:
                detect_if_false(board,old_column,old_row)
                return False
        
        detect_if_false(board,old_column,old_row)
        self.true_moves = moves
        return False

    def move_piece(self, x, y,old_column,old_row,board):

        capture_sound = pygame.mixer.Sound(r".\sounds\capture.mp3")
        piece_move_sound = pygame.mixer.Sound(r".\sounds\move-self.mp3")
        castling_sound = pygame.mixer.Sound(r".\sounds\castling_sound.mp3")
        check_sound = pygame.mixer.Sound(r".\sounds\check_sound.mp3")
        silly_sound = pygame.mixer.Sound(r".\sounds\troll_sound.mp3")

        did_capture = False
        if self.is_legal_move(x,y,board):
            #Calcular coordenadas nuevas 
            new_x,new_y = self.get_new_coordinates(x,y)
            self.old_positions = self.get_coordinates_x_y()
            self.did_legal_move = True

            self.row = new_x
            self.col = new_y

            #Movimientos especiales
            if self.name == 'pawn':
                if self.has_done_en_passant:
                    board.make_en_passant(self,new_x,new_y)

            if self.name == 'king':
                self.has_moved = True
                if self.can_castle_array != None and int(len(self.can_castle_array)) > 0:
                    for condition in self.can_castle_array:
                        if condition and not self.has_castled:
                            board.castle(self,new_y)
                            castling_sound.play()
                            self.can_castle_array = None
            #Movimientos especiales



            if self.name == 'rook':
                self.has_moved = True
            
            if self.name == 'pawn':
                self.has_moved = True
                if self.promo_rank == self.row:
                    self.promoted = True

            board.moved_piece = self
            self.deselect()
            

            if board.moved_piece.name == 'pawn' and board.moved_piece.has_promoted():
                board.promote(board.moved_piece,old_row,old_column)

            elif board.moved_piece.name in ('pawn','rook','queen','king','knight','bishop'):

                if isinstance(board.virtual_board[board.moved_piece.get_row()][board.moved_piece.get_column()],Piece) and not board.is_ally_piece(self,board.virtual_board[board.moved_piece.get_row()][board.moved_piece.get_column()]):
                    did_capture = True
                    #Aumentar contador de piezas por cada jugador de forma individual
                    if board.current_player_color == 'black':
                        board.black_player.counter_increase(board.virtual_board[board.moved_piece.get_row()][board.moved_piece.get_column()])
                    if board.current_player_color == 'white':
                        board.white_player.counter_increase(board.virtual_board[board.moved_piece.get_row()][board.moved_piece.get_column()])
                        
                board.update_board_status(old_row,old_column,board.moved_piece.get_column(),board.moved_piece.get_row(),board.moved_piece)

            
            board.move_counter += 1
            board.current_player_color = 'black' if board.current_player_color == 'white' else 'white'
        
            board.generate_moves() #Generar movimientos del tablero
            
            print("\n \n")
            print("Impresion de la  copia del tablero en el metodo move_piece")
            board_copy = board.new_copy()

            board_copy.generate_moves()


            board_copy.print_board()
            print("\n \n")
            
            enemy_pieces = board_copy.get_pieces()
            king = board_copy.get_king()
            actual_king = board.get_king()

            actual_king_row = actual_king.get_row()
            actual_king_column = actual_king.get_column()

            
            valid_moves_king = board_copy.get_valid_moves_king(king,enemy_pieces)
            print(f"Movimientos validos del rey: {valid_moves_king}")

            board.virtual_board[actual_king_row][actual_king_column].assign_moves(valid_moves_king)
            board_copy.virtual_board[king.get_row()][king.get_column()].assign_moves(actual_king.moves)
            ally_pieces = board_copy.get_pieces(get_ally_pieces = True)
            is_check= board.is_in_check(actual_king,enemy_pieces)
            if board.checked_status:
                check_sound.play()
            elif did_capture:
                capture_sound.play()
            else:
                piece_move_sound.play()

            board.checkmate = board.is_checkmate(actual_king,enemy_pieces,ally_pieces)

            
        else:
            self.deselect()
            board.generate_moves()
            if board.checked_status:
                silly_sound.play()
            
                    
    def show_squares(self,board):

        transparent_surface = pygame.Surface((SIZE,SIZE),pygame.SRCALPHA)
        special_surface = pygame.Surface((SIZE,SIZE), pygame.SRCALPHA)
        en_passant_surface = pygame.Surface((SIZE,SIZE),pygame.SRCALPHA)

        alpha_value = 100

        green_with_alpha = TRANSPARENT_GREEN + (alpha_value,)
        blue_with_alpha = TRANSPARENT_BLUE + (alpha_value,)
        red_with_alpha = TRANSPARENT_RED + (alpha_value,)

        if self.name == 'pawn':
            if board.check_if_en_passant() and self.show_en_passant != None:
                coord_x,coord_y = SIZE * self.show_en_passant[1],SIZE*self.show_en_passant[0]
                en_passant_surface.fill(red_with_alpha)
                self.surface.blit(en_passant_surface,(coord_x,coord_y))

        #MOSTRAR CUADROS DEL ENROQUE
        if self.name == 'king':
            main_board_enemy_pieces = board.get_pieces()
            rooks = board.get_rooks_for_castling(self)
            castling_condition_array = []
            if int(len(rooks)) > 0:
                for rook in rooks:
                    castling_condition_array.append(board.check_if_castle(self,rook,main_board_enemy_pieces))

                if int(len(castling_condition_array)) > 0:
                    special_surface.fill(blue_with_alpha)
                    for rook,condition in zip(rooks,castling_condition_array):
                        for key,castling_square in self.castling_squares.items():
                            if key == rook.col and condition:
                                coord_x,coord_y = SIZE*castling_square[1],SIZE*castling_square[0]
                                self.surface.blit(special_surface,(coord_x,coord_y))

        showable_moves = self.moves
        #No mostrar movimientos en donde se resalte una casilla con una pieza aliada
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

    def get_legal_moves(self,board):
        possible_moves = self.moves

        for move in self.moves:
            square = board.virtual_board[move[0]][move[1]]
            if isinstance(square,Piece) and board.is_ally_piece(self,square):
                possible_moves.remove(move)
        
        return possible_moves
    
    def clone(self):
        pass

    def restart_move_status(self):
        self.did_legal_move = False
    
    def get_new_position(self):
        x = SIZE * self.col
        y = SIZE * self.row
        return x,y



