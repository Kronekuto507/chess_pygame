import pygame
from pygame.locals import *
from classes_pieces.Piece import Piece
from classes_pieces.Bishop import Bishop
from classes_pieces.King import King
from classes_pieces.Queen import Queen
from classes_pieces.Knight import Knight
from classes_pieces.Rook import Rook
from classes_pieces.Pawn import Pawn
from .constants import *
import numpy as np
from copy import deepcopy

#Problemas con el jaque: Siempre hay jaquemate incluso si es posible tapar el jaque con una pieza o capturar la pieza
#Utilizar el método copy() para que compruebe la instancia del tablero en el siguiente turno. Actualizar el tablero real si el movimiento que se va a realizar es posible, de ser el caso que no lo sea, no se actualiza y por lo tanto no se procede al siguiente turno
class Board:
    
    def __init__(self, screen,white_player,black_player):
        #Plantilla en donde se dibujara el resto de cuadros
        #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        
        self.moved_piece = None
        self.selected_piece = None

        self.screen = screen
        self.white_player = white_player
        self.black_player = black_player
        self.checked_status = False
        self.current_player_color = 'white'
        self.move_counter = 0
        self.checkmate = False
        b_starter_row = 0
        
        self.sound_detect = 0

        self.current_king = None
        self.current_enemy_pieces = None
        self.board_start_game = 0
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
                self.draw_cell(self.screen,CREMA,coord_x,coord_y)

        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece):
                    piece.set_image()
    
    def internal_logic_of_selection(self):
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece) and piece.is_selected:
                    self.selected_piece = piece

    def create_virtual_board(self):
        
        for row in range(ROWS):
            self.virtual_board.append([])
            for col in range(COLS):
                    if row == 6:
                        w_pawn = Pawn('white',self.screen,row,col)
                        self.virtual_board[row].append(w_pawn)
                        self.virtual_board[row][col].create_image()
                        self.virtual_board[row][col].starting_square = self.virtual_board[row][col].get_starting_square_coordinates()
                    elif row == 1:
                        b_pawn = Pawn('black', self.screen,row,col)
                        self.virtual_board[row].append(b_pawn)
                        self.virtual_board[row][col].create_image()
                        self.virtual_board[row][col].starting_square = self.virtual_board[row][col].get_starting_square_coordinates()
        
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

        
    def is_ally_piece(self,main_piece,other_piece):
        return True if main_piece.color == other_piece.color and isinstance(other_piece,Piece) else False
                
    
    def select_piece_on_board(self,x,y):
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece) and piece.color == self.current_player_color:
                    if self.selected_piece == None: #Se detecta si no existe ya un objeto seleccionado, de ser el caso, seleccionar directamente
                        piece.select_piece(x,y)
                        
                    
                    else: #Si ya hay un objeto, este 
                        selected_row = piece.get_row()
                        selected_col = piece.get_column()
                    
                        self.virtual_board[selected_row][selected_col].deselect()
                        piece.select_piece(x,y)
                    
                

    def move_piece_on_board(self,x,y):
        
        old_column = 0
        old_row = 0

        if not self.checkmate:
            for row in self.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece) and piece.color == self.current_player_color: #COMPROBAR SI ES EL TURNO DEL JUGADOR
                        if piece.is_selected:
                            old_column = piece.get_column()
                            old_row = piece.get_row()
                            piece.move_piece(x,y,old_column,old_row,self)
                     
        
    def generate_moves(self):
        for row in self.virtual_board:
            for element in row:
                valid_types = (Rook,Knight,Bishop,Queen,King,Pawn)
                if isinstance(element,valid_types)  and hasattr(element,"generate_moves"):
                    moves = element.generate_moves(self)
                    element.assign_moves(moves)
    
    def assign_legal_moves(self):
        for row in self.virtual_board:
            for element in row:
                if isinstance(element,Piece):
                    legal_moves = element.get_legal_moves(self)
                    element.assign_moves(legal_moves)
                    

    def update_board_status(self,row,column,new_column,new_row,piece):

        self.virtual_board[row][column] = 0
        self.virtual_board[new_row][new_column] = piece
        self.virtual_board[new_row][new_column].row = new_row
        self.virtual_board[new_row][new_column].col = new_column  



    #Enrocar
    
    def set_current_player_color(self,player_color):
        self.current_player_color = player_color
    
    def promote(self,pawn,previous_row,previous_col):
        new_queen = Queen(pawn.color,pawn.surface,pawn.row,pawn.col)
        self.update_board_status(row=previous_row,column=previous_col,new_column=pawn.col,new_row=pawn.row,piece=new_queen)
        new_queen.create_image()

    def is_in_check(self,king,pieces):
        for piece in pieces:
            for move in piece.moves:
                
                if move[0] == king.get_row() and move[1] == king.get_column():
                    self.checked_status = True
                    

        if self.checked_status:
            #Para que no se repita el sonido de jaque indefinidamente
            self.sound_detect = 1
            return self.checked_status
        self.checked_status = False
        return self.checked_status
    
    def get_king(self):
        '''for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,King) and self.current_player_color == piece.color:
                    return piece'''
        
        return [piece for row in self.virtual_board for piece in row if isinstance(piece,King) and self.current_player_color == piece.color][0]


    def is_checkmate(self,king,enemy_pieces,ally_pieces):
        if not self.is_in_check(king,enemy_pieces):
            return False
        if king.moves:
            return False



        for piece in ally_pieces:
            legal_moves = piece.get_legal_moves(self)
            for move in legal_moves:
                board_instance = self.simulate_move(piece,move)

                board_instance.generate_moves()

                new_enemy_pieces = board_instance.get_pieces()
                
                board_instance.print_board()
                if not board_instance.is_in_check(king,new_enemy_pieces):
                    print("Impresion del tablero en el metodo is_checkmate")
                    board_instance.print_board()
                    return False
                del board_instance
                
        return True
        

    
    def get_moves(self,pieces):
        moves = []
        for piece in pieces:
            moves.extend(piece.moves)
        return moves
        
    def get_pieces(self,get_ally_pieces = False):
        pieces = []
        for row in self.virtual_board:
            for column in row:
                if not get_ally_pieces:
                    if isinstance(column,Piece) and column.color != self.current_player_color:
                            pieces.append(column)
                else:
                    if isinstance(column,Piece) and column.color == self.current_player_color:
                            pieces.append(column)
        return pieces
    
    def get_valid_moves_king(self,king,enemy_pieces): 

        valid_moves = king.get_legal_moves(self)

        legal_moves = deepcopy(king.get_legal_moves(self))

        for move in valid_moves:
            is_instance = self.simulate_move(king,move)
            get_king = is_instance.get_king()
            print(get_king.get_starting_square_coordinates())
            print("Impresion del tablero en el metodo get_valid_mvoes_king antes del if")
            print(f"Movimientos legales actuales: {legal_moves} movimiento a analizar: {move}")
            if is_instance.is_in_check(get_king,enemy_pieces):
                print("Impresion del tablero en el metodo get_valid_mvoes_king despues del if")
                is_instance.print_board()
                legal_moves.remove(move)
                
        return legal_moves
    
    def print_board(self):
        board_to_print = []

        for row in self.virtual_board:
            l = []
            for element in row:

                if isinstance(element,Piece) and element.color == 'white':
                    if element.name == 'king':
                        l.append('M')
                    else: 
                        l.append(element.name[0].upper())
                elif isinstance(element,Piece) and element.color == 'black':
                    if element.name == 'king':
                        l.append('m')
                    else:
                        l.append(element.name[0])

                if isinstance(element,int):
                    l.append(element)
            board_to_print.append(l)

        print(np.matrix(board_to_print))
        


    
    def create_copy(self):
        board_copy = Board(self.screen,self.white_player,self.black_player)
        '''for row in range(ROWS):
            row_to_append = []
            for col in range(COLS):
                row_to_append.append(self.virtual_board[row][col])
            board_copy.virtual_board.append(row_to_append)'''
        
        board_copy_virtual = [[col for col in row] for row in self.virtual_board]
        board_copy.virtual_board = board_copy_virtual
        board_copy.current_player_color = self.current_player_color
        return board_copy
    
    def new_copy(self):

        board_copy = Board(self.screen,self.white_player,self.black_player)
        '''for row in self.virtual_board:
            row_to_append = []
            for cell in row:
                if isinstance(cell,Piece):
                    copy  = cell.clone()
                    row_to_append.append(copy)
                else:
                    row_to_append.append(0)
            board_copy.virtual_board.append(row_to_append)'''
        

        board_copy_self_virtual_board = [[cell.clone() if isinstance(cell,Piece) else 0 for cell in row ] for row in self.virtual_board] #Crear copia del tablero virtual
        board_copy.virtual_board = board_copy_self_virtual_board #Asignarlo a la copia creada arriba

        board_copy.current_player_color = self.current_player_color
        return board_copy
    
    #Validar si esta en jaque despues de mover

    def validate_if_check_after_move(self,king):
        copy = self.create_copy()
        copy.generate_moves()
        check_status = copy.is_in_check(king,copy.get_pieces())
        return check_status
    
    def simulate_move(self,piece,move):
        instance = self.create_copy()
        piece_copy = piece.clone()
        instance.update_board_status(row=piece.get_row(),column=piece.get_column(),new_column=move[1],new_row=move[0],piece=piece_copy)
        return instance
    
    def check_if_castle(self,king,rook,enemy_pieces):

        if king.has_moved or rook.has_moved:
            return False
        if self.is_in_check(king,enemy_pieces):
            return False
        
        adyacent_moves = [(king.get_row(),king.get_column() + 1),(king.get_row(),king.get_column() - 1)]
        for adyacent_move in adyacent_moves:
            board = self.new_copy()
            board_copy_king = board.get_king()
            instance_simulation = board.simulate_move(board_copy_king,adyacent_move)
            if instance_simulation.is_in_check(board_copy_king,enemy_pieces):
                print("Impresion del tablero en el metodo check_if_castle")
                instance_simulation.print_board()
                return False
            
        king_col = king.get_column()
        
        rook_column = rook.get_column()

        king_side_empty = all(isinstance(self.virtual_board[king.get_row()][col], int) for col in range(king_col + 1, king_col + 3))
        queen_side_empty = all(isinstance(self.virtual_board[king.get_row()][col], int) for col in range(king_col - 1, king_col - 4, -1))

        if rook_column == 7:
            return king_side_empty
        if rook_column == 0:
            return queen_side_empty
        
        return False
    
    def castle(self,king,column):
        king_side_pos = 6
        queen_side_pos = 2

        def castling_logic(king,column,value = 5):
            self.virtual_board[king.row][column].col = value #Se asigna la columna nueva a la que se movera la torre
            rook = self.virtual_board[king.row][column] #Se almacena la torre en una variable auxiliar
            self.virtual_board[king.row][rook.col] = rook #Se intercambia la posicion del rey y la torre
            self.virtual_board[king.row][column] = 0 #La posicion de la torre original se actualiza a 0 en el programa
            
            self.virtual_board[king.row][rook.col].calc_pos()
            self.virtual_board[king.row][rook.col].has_moved = True
            king.has_moved = True
            king.calc_pos()

        if column == king_side_pos:
            castling_logic(king,COLS-1)

        elif column == queen_side_pos:
            castling_logic(king,0,value=3)
    
    def get_rooks_for_castling(self,king):
        rook_array = []
        '''for col in range(0,COLS):
            if isinstance(self.virtual_board[king.row][col],Rook):
                rook_array.append(self.virtual_board[king.row][col])'''

        rook_array = [element for element in self.virtual_board[king.row] if isinstance(element,Rook)]
        return rook_array
    
    def restart_move_status(self):
        self.virtual_board[self.moved_piece.get_row()][self.moved_piece.get_column()].restart_move_status()

    def check_if_en_passant(self):
        print(self.selected_piece)
        if self.moved_piece != None and self.selected_piece != None:
            piece = self.selected_piece.clone()
            if self.moved_piece.name == 'pawn':
                print(self.moved_piece.color)
                current_coordinates_moved_piece = self.moved_piece.get_starting_square_coordinates()
                print(current_coordinates_moved_piece)
                if piece.name == 'pawn':
                    print(piece.name)
                    current_selected_piece_coordinates = piece.get_starting_square_coordinates()
                    print(current_selected_piece_coordinates)
                    #variable para comparar la posicion
                    piece_next = current_selected_piece_coordinates if (current_coordinates_moved_piece[0], current_coordinates_moved_piece[1] + 1) == current_selected_piece_coordinates or (current_coordinates_moved_piece[0], current_coordinates_moved_piece[1] - 1) == current_selected_piece_coordinates else 0
                    var = True if isinstance(piece_next,tuple) else False
                    print(var)
                    if var and not piece.has_done_en_passant:
                        piece.show_en_passant = (current_coordinates_moved_piece[0] - 1,current_coordinates_moved_piece[1]) if self.moved_piece.color == 'black' else (current_coordinates_moved_piece[0] + 1,current_coordinates_moved_piece[1])
                        self.selected_piece.show_en_passant = piece.show_en_passant
                        return var
                
        return False
    
    def make_en_passant(self,pawn,row,col):
        print(f"({row}, {col})")
        en_passant_row = row + 1 if pawn.color == 'white' else row - 1
        self.virtual_board[en_passant_row][col] = 0


