import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.flag = RESIZABLE
        self.is_running = True
        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
    
    def run(self):
        chess_board = Board()
        while self.is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
            self.screen.fill(Color(225, 105,  255))
        
            
            chess_board.render_board(self.screen,WIDTH,HEIGHT)
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()