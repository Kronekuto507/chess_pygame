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

#Problemas con el jaque: Siempre hay jaquemate incluso si es posible tapar el jaque con una pieza o capturar la pieza
#Utilizar el método copy() para que compruebe la instancia del tablero en el siguiente turno. Actualizar el tablero real si el movimiento que se va a realizar es posible, de ser el caso que no lo sea, no se actualiza y por lo tanto no se procede al siguiente turno
class Board:
    
    def __init__(self, screen,white_player,black_player):
        #Plantilla en donde se dibujara el resto de cuadros
        #Diccionario que almacena las coordenadas de las superficie (Posiblemente innecesario, puede que lo elimine después)
        self.virtual_board = [] #Representacion virtual del tablero
        self.selected_piece = None
        self.moved_piece = None
        self.screen = screen
        self.white_player = white_player
        self.black_player = black_player
        self.checked_status = False
        self.current_player_color = 'white'
        self.move_counter = 0
        self.checkmate = False
        b_starter_row = 0

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


    def generate_pieces_moves(self, piece_arg):
        if piece_arg is (Rook,Knight,Bishop,Queen,King,Pawn) and hasattr(piece_arg,"generate_moves"):
            return piece_arg.generate_moves(self.virtual_board)
        
    def is_ally_piece(self,main_piece,other_piece):
        return True if main_piece.color == other_piece.color and isinstance(other_piece,Piece) else False
                
    
    def select_piece_on_board(self,x,y):
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,Piece) and piece.color == self.current_player_color:
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
        
        old_column = 0
        old_row = 0

        if self.board_start_game == 0:
            self.generate_moves()
            self.board_start_game += 1

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
                    legal_moves = element.make_legal_moves(self)
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
                    break

        if self.checked_status:
            return self.checked_status
        self.checked_status = False
        return self.checked_status
    
    def get_king(self):
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.virtual_board[row][col],King) and self.current_player_color == self.virtual_board[row][col].color:
                    self.virtual_board[row][col].row = row
                    self.virtual_board[row][col].col = col
                    return self.virtual_board[row][col]


    def is_checkmate(self,king,enemy_pieces,ally_pieces):
        if not self.is_in_check(king,enemy_pieces):
            return False
        if king.moves:
            return False
        
        for piece in ally_pieces:
            legal_moves = piece.get_legal_moves(self)
            for move in legal_moves:
                board_instance = self.simulate_move(piece,move)
                if not board_instance.is_in_check(king,enemy_pieces):
                    return False
                
            return True
        return False

    
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
        legal_moves = king.get_legal_moves(self)

        for move in valid_moves:
            is_instance = self.simulate_move(king,move)
            if is_instance.is_in_check(king,enemy_pieces):
                legal_moves.remove(move)
        return legal_moves
    
    def print_board(self):
        for row in self.virtual_board:
            print(row)
    
    def create_copy(self):
        board_copy = Board(self.screen,self.white_player,self.black_player)
        for row in range(ROWS):
            row_to_append = []
            for col in range(COLS):
                row_to_append.append(self.virtual_board[row][col])
            board_copy.virtual_board.append(row_to_append)
        board_copy.current_player_color = self.current_player_color
        return board_copy
    
    def new_copy(self):
        board_copy = Board(self.screen,self.white_player,self.black_player)

        for row in self.virtual_board:
            row_to_append = []
            for cell in row:
                if isinstance(cell,Piece):
                    copy  = cell.clone()
                    row_to_append.append(copy)
                else:
                    row_to_append.append(0)
            board_copy.virtual_board.append(row_to_append)
        board_copy.current_player_color = self.current_player_color
        return board_copy
    
    def validate_if_check_after_move(self,king):
        copy = self.create_copy()
        copy.generate_moves()
        check_status = copy.is_in_check(king,copy.get_pieces())
        return check_status
    
    def simulate_move(self,piece,move):
        instance = self.create_copy()
        instance.update_board_status(row=piece.get_row(),column=piece.get_column(),new_column=move[1],new_row=move[0],piece=piece)
        instance.generate_moves()
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
    
    def castle(self,king):
        king_side_pos = 6
        queen_side_pos = 2

        def castling_logic(king,column,value = 5):
            self.virtual_board[king.row][column].col = value #Se asigna la columna nueva a la que se movera la torre
            rook = self.virtual_board[king.row][column] #Se almacena la torre en una variable auxiliar
            self.virtual_board[king.row][rook.col] = rook #Se intercambia la posicion del rey y la torre
            self.virtual_board[king.row][column] = 0 #La posicion de la torre original se actualiza a 0 en el programa
            
            self.virtual_board[king.row][rook.col].calc_pos()
            self.virtual_board[king.row][rook.col].has_moved = True

        if king.col == king_side_pos:
            castling_logic(king,COLS-1)

        elif king.col == queen_side_pos:
            castling_logic(king,0,value=3)
    
    def get_rooks_for_castling(self,king):
        rook_array = []
        for col in range(0,COLS):
            if isinstance(self.virtual_board[king.row][col],Rook):
                rook_array.append(self.virtual_board[king.row][col])
        return rook_array

                

        








        




                            
            












            
            
                