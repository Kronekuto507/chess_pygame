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
                    print(x,y)
                    print(chess_board.virtual_board)
                    for row in range(ROWS):
                        for col in range(COLS):
                            if isinstance(chess_board.virtual_board[row][col],Piece):
                                chess_board.virtual_board[row][col].select_piece(x,y)
            self.screen.fill(CREMA)
            chess_board.draw_board(self.screen) 

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()