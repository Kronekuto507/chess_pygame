import pygame
from pygame.locals import *
import sys
from widgets.TextInput import TextInput
from widgets.Button import Button
from widgets.SubmitButton import SubmitButton
from widgets.Table import Table
from board.constants import *


def submit():
    pass

def create_user():
    from menu.Menu import Menu
    pygame.init()
    main_menu = Menu()
    MAIN_MENU_BUTTON = Button(x_pos=SCREEN_CENTER,y_pos=400,text="BACK TO MAIN MENU",
                            main_surface=SCREEN,base_color='white',hovering_color='green')
    SUBMIT_BUTTON = SubmitButton(x_pos=SCREEN_CENTER,y_pos=300,text="SUBMIT",main_surface=SCREEN,
                                 base_color='white',hovering_color='green')
    TEXT_INPUT_USER = TextInput(pos_x=SCREEN_CENTER,pos_y=100,screen=SCREEN,text_input_id=1)
    TEXT_INPUT_PASSWORD = TextInput(pos_x=SCREEN_CENTER,pos_y=150,screen=SCREEN,text_input_id=2,hide_text=True)

    widgets = [MAIN_MENU_BUTTON,SUBMIT_BUTTON,TEXT_INPUT_USER,TEXT_INPUT_PASSWORD]

    buttons = widgets[:2]
    text_inputs = widgets[2:]

    functions = [main_menu.render_menu,submit]

    button_dictionary = {button:foo for button,foo in zip(buttons,functions)}

    while True:
        SCREEN.fill((0,0,0))
        MOUSE_BUTTON_POS = pygame.mouse.get_pos()

        for widget in widgets:
            widget.render()        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button,function in button_dictionary.items():
                    if button.check_input(MOUSE_BUTTON_POS):
                        button.on_click_behaviour(function)

                for text_input in text_inputs:
                    print(MOUSE_BUTTON_POS)
                    text_input.select_text_input(MOUSE_BUTTON_POS)

            if event.type == pygame.KEYDOWN:
                for text_input in text_inputs:
                    if text_input.select_text_input(MOUSE_BUTTON_POS):
                        if event.key == pygame.K_BACKSPACE:
                            text_input.delete_char()
                        else:
                            print(event.unicode)
                            text_input.get_text(event.unicode)
            


        pygame.display.update()

def play():
    pass

def leader_board():
    pass

def quit():
    sys.exit()