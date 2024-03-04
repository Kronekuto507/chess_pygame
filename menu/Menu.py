import pygame
import sys
from pygame.locals import *
from widgets.Button import Button
from board.constants import *
from menu.menu_functions import *
from functools import partial


PLACE = 100
CREATE_USER = Button(x_pos=PLACE, y_pos=225, text="Create User", 
                    main_surface=SCREEN, base_color="white",hovering_color="green")
PLAY = Button(x_pos=PLACE,y_pos=275,text="Play",
                main_surface=SCREEN,base_color="white",hovering_color="black")
STATISTICS = Button(x_pos=PLACE,y_pos=325, text= "Statistics",
                    main_surface= SCREEN, base_color= "white", hovering_color = "green")
QUIT = Button(x_pos=PLACE,y_pos=400,text="Quit",main_surface=SCREEN,base_color="white",hovering_color="green")

FUNCTION_LIST = [create_user,play,leader_board,quit]
BUTTON_LIST = [CREATE_USER,PLAY,STATISTICS,QUIT]
DICTIONARY_BUTTONS = {button:foo for button,foo in zip(BUTTON_LIST,FUNCTION_LIST)}

class Menu():
    
    def render_menu(self):
        
        while True:
            SCREEN.blit(BG_1,(0,0))
            prov = pygame.font.SysFont("Arial",150)
            MOUSE_POS_MENU = pygame.mouse.get_pos()
            MENU_TEXT = prov.render("Chess",True, "white")
            MENU_RECT = MENU_TEXT.get_rect(center = (MENU_TEXT.get_width() - 150,100))
            
            
            SCREEN.blit(MENU_TEXT,MENU_RECT)

            for button in BUTTON_LIST:
                button.hover(MOUSE_POS_MENU)
                button.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for button,function in DICTIONARY_BUTTONS.items():
                        if button.check_input(MOUSE_POS_MENU):
                            button.on_click_behaviour(function)

            pygame.display.update()

        
