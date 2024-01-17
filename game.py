import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT,CREMA
from classes_pieces.Piece import *


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
        chess_board.generate_moves()
        counter_click = 0
        while self.is_running:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x,y = event.pos
                        print(counter_click)
                        print(x)
                        if counter_click == 0:
                            chess_board.select_piece_on_board(x,y)
                            counter_click += 1
                        else:
                            chess_board.move_piece_on_board(x,y)
                            counter_click = 0
            self.screen.fill(CREMA)
            chess_board.draw_board()
            #Si hay una pieza seleccionada, entonces esta muestra las celdas a las que puede ir  
            for row in chess_board.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece):
                        if piece.is_selected:
                            piece.show_squares()
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()