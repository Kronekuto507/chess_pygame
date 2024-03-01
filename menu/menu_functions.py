import pygame
from pygame.locals import *
import sys
from widgets.TextInput import TextInput
from widgets.Button import Button
from widgets.SubmitButton import SubmitButton
from widgets.Table import Table
from board.constants import *

from database.Query import Query
obtained_text = None


def submit():
    query = Query("user_info.sqlite")
    query.query('''
        CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255)
        );
    ''')
    name = obtained_text[0]
    passw = obtained_text[1]
    query.query(f'''
        INSERT INTO usuario (username,password) VALUES ('{name}','{passw}'); 
    ''')
    query.__del__()

def create_user():
    from menu.Menu import Menu
    pygame.init()
    main_menu = Menu()
    PLACE = 50
    MAIN_MENU_BUTTON = Button(x_pos=255 - PLACE ,y_pos=350,text="BACK TO MAIN MENU",
                            main_surface=SCREEN,base_color='white',hovering_color='green')
    SUBMIT_BUTTON = SubmitButton(x_pos= 130,y_pos=300,text="SUBMIT",main_surface=SCREEN,
                                 base_color='white',hovering_color='green')
    TEXT_INPUT_USER = TextInput(pos_x=PLACE,pos_y=100,screen=SCREEN,text_input_id=1)
    TEXT_INPUT_PASSWORD = TextInput(pos_x=PLACE,pos_y=150,screen=SCREEN,text_input_id=2,hide_text=True)

    widgets = [MAIN_MENU_BUTTON,SUBMIT_BUTTON,TEXT_INPUT_USER,TEXT_INPUT_PASSWORD]

    buttons = widgets[:2]
    text_inputs = widgets[2:]

    functions = [main_menu.render_menu,submit]

    button_dictionary = {button:foo for button,foo in zip(buttons,functions)}
    
    while True:
        MOUSE_BUTTON_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG_1,(0,0))

        for widget in widgets:
            widget.render()
        for button in buttons:
            button.hover(MOUSE_BUTTON_POS)        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button,function in button_dictionary.items():
                    if button.check_input(MOUSE_BUTTON_POS):
                        if isinstance(button,SubmitButton):
                            global obtained_text
                            obtained_text = button.get_from_text_input(TEXT_INPUT_USER,
                                                                       TEXT_INPUT_PASSWORD)
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




