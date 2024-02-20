import pygame
import sys
from pygame.locals import *
from utils.Button import Button
from board.constants import SCREEN
from menu_functions import *

CREATE_USER = Button(x_pos=250, y_pos=100, text="Create User", 
                    main_surface=SCREEN, base_color="white",hovering_color="green")
PLAY = Button(x_pos=250,y_pos=150,text="Play",
                main_surface=SCREEN,base_color="white",hovering_color="black")
LEADERBOARD = Button(x_pos=250,y_pos=200, text= "Leaderboard",
                    main_surface= SCREEN, base_color= "white", hovering_color = "green")
QUIT = Button(x_pos=250,y_pos=250,text="Quit",main_surface=SCREEN,base_color="white",hovering_color="green")

class Menu():
    def __init__(self):
        
        self.render_menu()
    
    def render_menu(self):
        while True:
            prov = pygame.font.SysFont("cambria",100)
            MOUSE_POS_MENU = pygame.mouse.get_pos()
            MENU_TEXT = prov.render("CHESS",True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center = (250,50))
            SCREEN.blit(MENU_TEXT,MENU_RECT)

            for button in [CREATE_USER,PLAY,LEADERBOARD,QUIT]:
                button.hover(MOUSE_POS_MENU)
                button.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CREATE_USER.check_input(MOUSE_POS_MENU):
                        create_user()
                    if PLAY.check_input(MOUSE_POS_MENU):
                        play()
                    if LEADERBOARD.check_input(MOUSE_POS_MENU):
                        leader_board()
                    if QUIT.check_input(MOUSE_POS_MENU):
                        quit()

        
