import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT,CREMA,ROWS,COLS
from classes_pieces.pieces import *


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
    
    def run(self):
        chess_board = Board()
        chess_board.create_virtual_board(self.screen)
        while self.is_running:
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    print('ABAJO')
                    x,y = event.pos

                    #Fragmento de codigo que selecciona la pieza
                    for row in range(ROWS):
                        for col in range(COLS):
                            if isinstance(chess_board.virtual_board[row][col],Piece):
                                if chess_board.selected_piece is None: #Se detecta si no existe ya un objeto seleccionado, de ser el caso, seleccionar directamente
                                    chess_board.virtual_board[row][col].select_piece(x,y)
                                else: #Si ya hay un objeto, este 
                                    selected_row = chess_board.selected_piece.get_row()
                                    selected_col = chess_board.selected_piece.get_column()

                                    chess_board.virtual_board[selected_row][selected_col].deselect()
                                    chess_board.virtual_board[row][col].select_piece(x,y)


                    
                    #asigna la pieca seleccionada en el fragmento de arriba al tablero
                    for row in range(ROWS):
                        for col in range(COLS):
                            if isinstance(chess_board.virtual_board[row][col],Piece):
                                print(chess_board.virtual_board[row][col].is_selected)
                                if chess_board.virtual_board[row][col].is_selected:
                                    chess_board.selected_piece = chess_board.virtual_board[row][col]
                    print(chess_board.selected_piece)
                                
            self.screen.fill(CREMA)
            chess_board.draw_board(self.screen) 

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()