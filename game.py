import pygame
from pygame.locals import *
from board.board_template import *
from classes_pieces.pawn import Pawn
width, height = 1000,1000

class Game:
    def __init__(self):
        pygame.init()
        self.flag = RESIZABLE
        self.is_running = True
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size, self.flag)
    
    def run(self):
        chess_board = Board()
        white_pawns = pygame.sprite.Group()
        white_pawn = Pawn("white",chess_board.surf_cord["surf_01"],chess_board.surf_cord["coordinate_01"][0],chess_board.surf_cord["coordinate_01"][1])
        white_pawns.add(white_pawn)
        while self.is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
            self.screen.fill(Color(225, 105,  255))
            
            white_pawns.draw(self.screen)
            white_pawns.update()
            
            chess_board.render_board(self.screen,width=width,height=height)
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()