import pygame
from pygame.locals import *
from menu.Menu import Menu


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    game_menu = Menu()
    game_menu.render_menu()