import pygame
from pygame.locals import *
from database.Query import Query
from widgets.Button import Button
from widgets.TextInput import TextInput
from board.constants import *
import sys

class StatMenu:
    def render(self):
        from menu.Menu import Menu
        pygame.init()
        MENU = Menu()
        search_bar = TextInput(pos_x=150,pos_y=25,screen=SCREEN,text_input_id=9,width=360)
        search_button = Button(x_pos=375,y_pos=100,text="Search",main_surface=SCREEN,base_color="white",hovering_color="pink")
        back_to_menu = Button(x_pos=150,y_pos=100,text="Back to Menu",main_surface=SCREEN,base_color="white",hovering_color="blue")

        widgets = [search_bar,search_button,back_to_menu]
        buttons = widgets[-2:]
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.blit(BG_1,(0,0))
            functions = [lambda: self.show_stats(search_bar.return_text(),search_bar),MENU.render_menu]
            button_function_dictionary = {button : foo for button,foo in zip(buttons,functions)}
            for widget in widgets:
                widget.render()
            for button in buttons:
                button.hover(MOUSE_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exist()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Iterar en el diccionario
                    for button,function in button_function_dictionary.items():

                        if button.check_input(MOUSE_POS):
                            button.on_click_behaviour(function)

                    search_bar.select_text_input(MOUSE_POS)
                if event.type == pygame.KEYDOWN:
                    if search_bar.select_text_input(MOUSE_POS):
                        if event.key == pygame.K_BACKSPACE:
                            search_bar.delete_char()
                        else:
                            search_bar.get_text(event.unicode)
            pygame.display.update()


    def show_stats(self,username,text_input):
        info = self.database(username,text_input)

        if info == None:
            pass
        else:
            from menu.Menu import Menu
            MENU = Menu()
            return_button = Button(x_pos=375,y_pos=35,text="Go Back",main_surface=SCREEN,base_color="white",hovering_color="pink")
            back_to_menu = Button(x_pos=150,y_pos=35,text="Back to Menu",main_surface=SCREEN,base_color="white",hovering_color="blue")
            FUENTE = pygame.font.SysFont('Arial',30)
            buttons = [return_button,back_to_menu]
            text_to_display = [
                'Username: ' + info[1],
                'Wins: ' + str(info[2]),
                'Loses:' + str(info[3]),
                'Total of Pieces Captured: ' + str(info[4]),
                'Total Time played:  ' + str(info[5])
            ]
            position_text_dictionary = {text:(100,50+(index*35)) for index,text in enumerate(text_to_display)}
            functions = [self.render,MENU.render_menu]
            button_func_dictionary = {button:foo for button,foo in zip(buttons,functions)}

            while True:
                MOUSE_POS = pygame.mouse.get_pos()
                SCREEN.blit(BG_1,(0,0))
                
                for button in buttons:
                    button.render()
                    button.hover(MOUSE_POS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exist()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button,function in button_func_dictionary.items():
                            if button.check_input(MOUSE_POS):
                                button.on_click_behaviour(function)

                for text,rect in position_text_dictionary.items():
                    display_text = FUENTE.render(text,True,'white')
                    SCREEN.blit(display_text,rect)
                    
                pygame.display.update()
    
    def database(self,username,text_input):
        import sqlite3
        query = Query(primary_database)
        fetched_info = None
        try:
            query.query(f'''
                SELECT * FROM user_stats WHERE user = '{username}'
            ''')
            fetched_info = query.fetch_one()
        except sqlite3.Error as e:
            print(e)
        finally:
            query.__del__()
            text_input.restart_text()
            return fetched_info
            



                        

            
