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
        return True if main_piece.color == other_piece.color else False
                
    
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
        self.generate_moves()
        enemy_pieces = self.get_pieces()
        king = self.get_king()
        is_check = self.is_in_check(king,enemy_pieces)
        valid_moves_king = self.get_valid_moves_king(king,enemy_pieces)
        self.virtual_board[king.get_row()][king.get_column()].assign_moves(valid_moves_king)
        self.checkmate = False
        if self.move_counter >= 2:
            self.checkmate = self.is_checkmate(king,enemy_pieces)

        if not self.checkmate:
            for row in self.virtual_board:
                for piece in row:
                    if not is_check:
                        if isinstance(piece,Piece) and piece.color == self.current_player_color: #COMPROBAR SI ES EL TURNO DEL JUGADOR
                            if piece.is_selected:
                                old_column = piece.get_column()
                                old_row = piece.get_row()
                                piece.move_piece(x,y,self)
                                if piece.name == 'pawn':
                                    piece.has_moved = True
                                self.moved_piece = piece
                                piece.deselect()
                                self.move_counter += 1
                    else:
                        if isinstance(piece,Piece) and piece.color == self.current_player_color:
                            self.checked_status = True
                            old_column,old_row,piece = self.move_logic_for_check(enemy_pieces,x,y,king,piece)
                        

            if self.moved_piece.name == 'pawn' and self.moved_piece.has_promoted():
                self.promote(self.moved_piece,old_row,old_column)

            elif self.moved_piece.name in ('pawn','rook','queen','king','knight','bishop'):
                self.update_board_status(old_row,old_column,self.moved_piece.get_column(),self.moved_piece.get_row(),self.moved_piece)
        
                     
        
    def generate_moves(self):
        for row in self.virtual_board:
            for element in row:
                valid_types = (Rook,Knight,Bishop,Queen,King,Pawn)
                if isinstance(element,valid_types)  and hasattr(element,"generate_moves"):
                    moves = element.generate_moves(self)
                    element.assign_moves(moves)

    def update_board_status(self,row,column,new_column,new_row,piece):

        piece_capture_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\capture.mp3")
        piece_move_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\move-self.mp3")

        if isinstance(self.virtual_board[new_row][new_column],int):
            piece_move_sound.play()
        elif not self.is_ally_piece(self.virtual_board[row][column],self.virtual_board[new_row][new_column]):
            piece_capture_sound.play()

        self.virtual_board[row][column] = 0
        self.virtual_board[new_row][new_column] = piece
        self.virtual_board[new_row][new_column].calc_pos()

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
                    return self.checked_status
                
        self.checked_status = False
        return self.checked_status
    
    def get_king(self):
        for row in self.virtual_board:
            for piece in row:
                if isinstance(piece,King) and self.current_player_color == piece.color:
                    return piece


    def is_checkmate(self,king,pieces):
        if not self.is_in_check(king,pieces):
            return False
        
        if king.moves:
            return True
        

    def get_pieces(self,enemy_pieces = True):
        pieces = []
        for row in self.virtual_board:
            for column in row:
                if enemy_pieces:
                    if isinstance(column,Piece) and column.color != self.current_player_color:
                        pieces.append(column)
                else:
                    if isinstance(column,Piece) and column.color == self.current_player_color:
                        pieces.append(column)
        for piece in pieces:
            print(f"{piece.color} and {piece.name}")
        return pieces
    
    def move_logic_for_check(self,enemy_pieces,x,y,king,selected_piece):

        attacking_pieces = []
        old_column = selected_piece.get_column()
        old_row = selected_piece.get_row()
        for piece in enemy_pieces:
            for move in piece.moves:
                if move[0] == king.get_row() and move[1] == king.get_column():
                    attacking_pieces.append(piece)

        aux_piece = selected_piece
        aux_piece.move_piece(x,y,self)
        row = aux_piece.get_row()
        col = aux_piece.get_column()

        if selected_piece.is_selected:
            if selected_piece.name != 'king':
                for move in selected_piece.moves:
                    for attacking_piece in attacking_pieces:
                        for attacking_move in attacking_piece.moves:
                            if move == attacking_move or move[0]==attacking_piece.get_row() and move[1] == attacking_piece.get_column():
                                selected_piece.move_piece(x,y,self)
            if selected_piece.name == 'king':
                selected_piece.move_piece(x,y,self)
        
        self.moved_piece = selected_piece
        selected_piece.deselect()
        self.move_counter += 1
        self.checked_status = False
        return old_column,old_row,selected_piece

        
    
    def check_next_turn(self,x,y):
        board_copy_analysis = self.virtual_board.copy()
        for row in board_copy_analysis:
            for piece in row:
                #if not self.is_in_check(king,enemy_pieces):
                if isinstance(piece,Piece) and piece.color == self.current_player_color: #COMPROBAR SI ES EL TURNO DEL JUGADOR
                    if piece.is_selected:
                        piece.move_piece(x,y,self)
                        if piece.name == 'pawn':
                            piece.has_moved = True
                        piece.deselect()
        return board_copy_analysis
    
    def get_valid_moves_king(self,king,enemy_pieces): #HAY UN BUG CON EL PEON
        valid_moves = king.moves
        for piece in enemy_pieces:
            for move in king.moves:
                for piece_move in piece.moves:
                    if move == piece_move:
                        valid_moves.remove(move)
        return valid_moves




        




                            
            












            
            
                