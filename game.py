import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT,CREMA
from classes_pieces.pieces import *


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
    #Aniluz
    def run(self):
        chess_board = Board(self.screen)
        chess_board.create_virtual_board()
        piece_capture_sound = pygame.mixer.Sound(r"C:\Users\aaron\Desktop\Programacion\Python\ajedrez\sounds\capture.mp3")
        while self.is_running:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print('ABAJO')
                        x,y = event.pos

                        #Fragmento de codigo que selecciona la pieza
                        for row in chess_board.virtual_board:
                            for piece in row:
                                if isinstance(piece,Piece):
                                    if chess_board.selected_piece is None: #Se detecta si no existe ya un objeto seleccionado, de ser el caso, seleccionar directamente
                                        piece.select_piece(x,y)
                                    else: #Si ya hay un objeto, este 
                                        selected_row = piece.get_row()
                                        selected_col = piece.get_column()
                                        chess_board.virtual_board[selected_row][selected_col].deselect()
                                        piece.select_piece(x,y)

                        #asigna la pieca seleccionada en el fragmento de arriba al tablero
                        for row in chess_board.virtual_board:
                            for piece in row:
                                if isinstance(piece,Piece):
                                    print(piece.is_selected)
                                    if piece.is_selected:
                                        chess_board.selected_piece = piece
                        print(chess_board.selected_piece)
                    elif event.button == 3:
                        x,y = event.pos
                        for row in chess_board.virtual_board:
                            for piece in row:
                                if isinstance(piece,Piece):
                                    if piece.is_selected:
                                        old_column = piece.get_column()
                                        old_row = piece.get_row()
                                        piece.move_piece(x,y)
                                        piece.deselect()
                                        chess_board.virtual_board[old_row][old_column] = 0
                                        new_column = piece.get_column()
                                        new_row = piece.get_row()
                                        if not isinstance(chess_board.virtual_board[new_row][new_column], int):
                                            piece_capture_sound.play()
                                        chess_board.virtual_board[new_row][new_column] = piece
                    for row in chess_board.virtual_board:
                        print(row)
                        
                                        


            #Dibujar tablero
            self.screen.fill(CREMA)
            chess_board.draw_board()
            #Si hay una pieza seleccionada, entonces esta muestra las celdas a las que puede ir  
            '''for row in chess_board.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece):
                        piece.show_squares()'''
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()