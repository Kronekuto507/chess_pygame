import pygame
from pygame.locals import *
from board.chess import *
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
        while self.is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
            self.screen.fill(Color(225, 105,  255))
            
            chess_board.render_board(self.screen,width=width,height=height)
            
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()