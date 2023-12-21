import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        pygame.init()
        self.flag = RESIZABLE
        self.is_running = True
        self.size = (500, 500)
        self.screen = pygame.display.set_mode(self.size, self.flag)
    
    def run(self):
    
        while self.is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
            self.screen.fill(Color(225, 105,  255))
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()