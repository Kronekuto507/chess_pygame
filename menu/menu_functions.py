import pygame
from pygame.locals import *
import sys
from widgets.TextInput import TextInput
from widgets.Button import Button
from widgets.SubmitButton import SubmitButton
from board.constants import *
from database.Query import Query
obtained_text = None


def submit():
    query = Query(primary_database)
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

def behaviour_after_clicking_play(text_input_dictionary):
    from menu.game import Game
    import sqlite3
    query = Query(primary_database)
    match_found = False
    match_counter = 0
    #Para facilitar el manejo de excepciones, se simplifca el diccionary a una lista de elementos individuales:
    to_list = list(text_input_dictionary.items())
    #Transformar a una lista de valores individuales para reiniciar los text_input
    text_inputs = [text_input for tuple in to_list for text_input in tuple]
    #Retornar informacion de la lista en tuplas con texto
    get_information = [(element[0].return_text(),element[1].return_text()) for element in to_list]
    try:
        for information in get_information:
            username = information[0]
            password = information[1]
            query.query(f'''SELECT username, password FROM usuario WHERE username = '{username}' AND password = '{password}' ''')
            if query.fetch_one():
                match_counter += 1
                if match_counter == 2:
                    match_found = True
    except sqlite3.Error as e:
        print(e)
        for text_input in text_inputs:
            text_input.restart_text()
    else:
        if match_found:
            print("TODO PERFECTO")
            GAME = Game(SCREEN)
            GAME.set_players(player_1=get_information[0][0],player_2=get_information[1][0])
            GAME.run()
        else:
            for text_input in text_inputs:
                text_input.restart_text()
    finally:
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
    TEXT_INPUT_USER = TextInput(pos_x=PLACE,pos_y=100,screen=SCREEN,text_input_id=1,width=360)
    TEXT_INPUT_PASSWORD = TextInput(pos_x=PLACE,pos_y=150,screen=SCREEN,text_input_id=2,width=360,hide_text=True)

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
                            text_input.get_text(event.unicode)
            


        pygame.display.update()

def play():
    from menu.Menu import Menu
    pygame.init()

    MENU = Menu()

    #CREAR TEXT_INPUT
    USER_TEXT_INPUT_LEFT = TextInput(pos_x=50,pos_y=150,screen=SCREEN,text_input_id=3,width=200)
    USER_TEXT_INPUT_RIGHT = TextInput(pos_x=350,pos_y=150,screen=SCREEN,text_input_id=4,width=200)

    PASSWORD_TEXT_INPUT_LEFT = TextInput(pos_x=50,pos_y=200,screen=SCREEN,text_input_id=5,width=200,hide_text=True)
    PASSWORD_TEXT_INPUT_RIGHT = TextInput(pos_x=350,pos_y=200,screen=SCREEN,text_input_id=6,width=200,hide_text=True)

    #CREAR_BOTONES
    PLAY_BUTTON = Button(x_pos=300,y_pos=500,text="Play Chess",
                        main_surface=SCREEN,base_color="white",hovering_color="blue")
    BACK_BUTTON = Button(x_pos=300,y_pos=550,text="Back to Menu",
                        main_surface=SCREEN,base_color="white",hovering_color="blue")
    
    buttons = [PLAY_BUTTON,BACK_BUTTON]


    text_inputs = [USER_TEXT_INPUT_LEFT,
                   PASSWORD_TEXT_INPUT_LEFT,
                   USER_TEXT_INPUT_RIGHT,
                   PASSWORD_TEXT_INPUT_RIGHT]
    

    text_input_dict = {USER_TEXT_INPUT_LEFT: PASSWORD_TEXT_INPUT_LEFT,USER_TEXT_INPUT_RIGHT:PASSWORD_TEXT_INPUT_RIGHT}

    widgets = buttons + text_inputs

    #Crear imagenes para luego escalarlas
    BLACK_KING = pygame.image.load(r".\images\black_king.jpg").convert_alpha()
    WHITE_KING = pygame.image.load(r".\images\white_king.jpg").convert_alpha()

    BLACK_KING_SCALED = pygame.transform.scale(BLACK_KING,(200,200))
    WHITE_KING_SCALED = pygame.transform.scale(WHITE_KING,(200,200))

    while True:

        SCREEN.fill((0,0,0))
        MOUSE_BUTTON_POS = pygame.mouse.get_pos()
        SCREEN.blit(BLACK_KING_SCALED,(50,250))
        SCREEN.blit(WHITE_KING_SCALED,(350,250))

        functions = [lambda:behaviour_after_clicking_play(text_input_dict),MENU.render_menu]
        dictionary = {button:foo for button,foo in zip(buttons,functions)}

        for widget in widgets:
            widget.render()
        for button in buttons:
            button.hover(MOUSE_BUTTON_POS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Click behaviour for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Click behaviour for buttons
                for button,function in dictionary.items():
                    if button.check_input(MOUSE_BUTTON_POS):
                        button.on_click_behaviour(function)
                #Click behaviour for text_inputs
                for text_input in text_inputs:
                    text_input.select_text_input(MOUSE_BUTTON_POS)
            if event.type == pygame.KEYDOWN:
                #behvaiour when we write inside the text input
                for text_input in text_inputs:
                    if text_input.select_text_input(MOUSE_BUTTON_POS):
                        if event.key == pygame.K_BACKSPACE:
                            text_input.delete_char()
                        else:
                            text_input.get_text(event.unicode)
        pygame.display.update()



def leader_board():
    pass

def quit():
    sys.exit()




