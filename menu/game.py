import pygame
from pygame.locals import *
from board.board_template import *
from classes_pieces.Piece import Piece
from player.player_class import Player
from widgets.Button import Button
import sys
import time
from database.Query import Query

class Game:
    def __init__(self,screen):
        pygame.init()
        self.is_running = True
        self.screen = screen
        self.players = None
    #Aniluz
    def run(self):
        chess_board = Board(self.screen,self.players[0],self.players[1])
        chess_board.create_virtual_board()
        chess_board.generate_moves()
        clock = pygame.time.Clock()

        while self.is_running:
            self.screen.fill(VERDE)
            chess_board.draw_board()         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        x,y = event.pos
                        chess_board.select_piece_on_board(x,y)
                        chess_board.internal_logic_of_selection()
                    elif event.button == 3:
                        x,y = event.pos
                        chess_board.move_piece_on_board(x,y)

            #Animacion
            if chess_board.moved_piece != None:
                if chess_board.moved_piece.did_legal_move:

                    new_x,new_y = chess_board.moved_piece.get_new_position()
                    old_x,old_y = chess_board.moved_piece.old_positions
                    chess_board.moved_piece.pos_x = old_x
                    chess_board.moved_piece.pos_y = old_y

                    while(chess_board.moved_piece.pos_x != new_x or chess_board.moved_piece.pos_y != new_y):
                        chess_board.moved_piece.animate()
                        self.screen.fill(VERDE)
                        chess_board.draw_board()
                        pygame.display.update()
                        clock.tick(60)

                    chess_board.restart_move_status()

            if chess_board.checkmate:
                chess_board.fin = time.time() - chess_board.inicio_tiempo
                if chess_board.current_player_color == 'white':
                    chess_board.winner = chess_board.black_player
                    chess_board.black_player.set_win()
                    chess_board.white_player.set_lose()
                else:
                    chess_board.winner = chess_board.white_player
                    chess_board.white_player.set_win()
                    chess_board.black_player.set_lose()
                self.end_game_screen(chess_board.fin,chess_board)
            
            #Si hay una pieza seleccionada, entonces esta muestra las celdas a las que puede ir  
            for row in chess_board.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece):
                        if piece.is_selected:
                            piece.show_squares(chess_board)
            
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

    def end_game_screen(self,time,board):
        from menu.Menu import Menu
        MENU = Menu()
        fuente = pygame.font.SysFont("Arial",15)

        BACK_TO_MENU = Button(x_pos=300,y_pos=500,text='Back to Menu',
                            main_surface=SCREEN,base_color='white',hovering_color='blue')
        PLAY_AGAIN = Button(x_pos=300,y_pos=400,text='Play Again',
                            main_surface=SCREEN,base_color='white',hovering_color='blue')
        
        spacing = 25

        buttons = [BACK_TO_MENU,PLAY_AGAIN]
        functions = [MENU.render_menu,self.run]
        button_func_dictionary = {button:foo for button,foo in zip(buttons,functions)}
        
        #Renderizar tiempo 
        time_lasted = fuente.render('Tiempo que duro: ' + str(time),True,'white')
        time_lasted_rect = time_lasted.get_rect(center = (300,50))
        #Renderizar movimientos realizados
        moves_done = fuente.render('Movimientos realizados' + str(board.move_counter),True,'white')
        moves_done_rect = moves_done.get_rect(center = (300,50 + spacing))
        #Renderizar piezas capturadas
        count_all_captures = 0
        for values_black,values_white in zip(board.black_player.captured_pieces.values(),board.white_player.captured_pieces.values()):
            count_all_captures += values_black + values_white

        captured_pieces = fuente.render('Total de piezas capturadas: ' + str(count_all_captures) ,True,'white')
        captured_pieces_rect = captured_pieces.get_rect(center = (300, 50 + 2*spacing))

        #Renderizar piezas negras:
        texto_lista_negras = list(board.black_player.captured_pieces.items())
        '''Se le da formato al texto que se imprimira'''
        texto_lista_negras = ['Piece: ' + element[0][0].upper() + element[0][1:] + 's amount: ' + str(element[1]) for element in texto_lista_negras]
        ''''Se agrega el texto con su respectiva posicion'''
        diccionario_negras = {texto:(25,125 + (index*15)) for index,texto in enumerate(texto_lista_negras)}

        #Renderizar piezas blancas
        texto_lista_blancas = list(board.white_player.captured_pieces.items())
        '''Se le da formato al texto que se imprimira: el primer elemento de la tupla es el nombre del tipo de pieza. El segundo es la cantidad'''
        texto_lista_blancas = ['Piece: ' + element[0][0].upper() + element[0][1:] + 's amount: ' + str(element[1]) for element in texto_lista_blancas]
        '''Se agrega el texto con su respectiva posicion'''
        diccionario_blancas = {texto:(300,125+(index*15)) for index,texto in enumerate(texto_lista_blancas)}

        #Renderizar ganador
        winner = fuente.render('The winner is ' + board.winner.name + ' whose color is ' + board.winner.player_color,True,'white')
        winner_rect = winner.get_rect(center = (300,30))

        #Renderizar nombre de jugadores
        name_black = fuente.render('Black: ' + board.black_player.name,True,'white')
        name_white = fuente.render('White: ' + board.white_player.name,True,'white')

        self.get_info_to_database(player_1=board.black_player,player_2=board.white_player,time=time)

        while True:
            SCREEN.blit(BG_1,(0,0))
            MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.blit(time_lasted,time_lasted_rect)
            SCREEN.blit(moves_done,moves_done_rect)
            SCREEN.blit(captured_pieces,captured_pieces_rect)
            SCREEN.blit(winner,winner_rect)
            SCREEN.blit(name_black,(25,110))
            SCREEN.blit(name_white,(300,110))
            #Renderizar los botones
            for button in buttons:
                button.render()
                button.hover(MOUSE_POS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    for button,function in button_func_dictionary.items():
                        if button.check_input(MOUSE_POS):
                            button.on_click_behaviour(function)

            for texto,rect in diccionario_negras.items():
                surface = fuente.render(texto,True,'white')
                SCREEN.blit(surface,rect)

            for texto,rect in diccionario_blancas.items():
                surface = fuente.render(texto,True,'white')
                SCREEN.blit(surface,rect)

            board.black_player.reset_counter()
            board.white_player.reset_counter()
            board.black_player.reset_win()
            board.white_player.reset_win()
            board.black_player.reset_lose()
            board.white_player.reset_lose()
            pygame.display.update()

    def set_players(self,player_1,player_2):
        self.players = [Player('white',player_2),Player('black',player_1)]
        print(self.players)

    def get_info_to_database(self,player_1,player_2,time):
        import sqlite3

        query = Query(primary_database)
        query.query('''CREATE TABLE IF NOT EXISTS user_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user VARCHAR(255) UNIQUE,
                        wins INTEGER,
                        loses INTEGER,
                        amount_captured INTEGER,
                        time INTEGER,
                        FOREIGN KEY(user) REFERENCES usuario(username)
            )''')
        
        try:
            get_user_if_exist_first = query.query(f'''
                        SELECT COUNT(*) FROM user_stats WHERE user = '{player_1.name}'
                        ''')
            first_count = query.fetch_one()[0]
            get_user_if_exist_second = query.query(f'''
                        SELECT COUNT(*) FROM user_stats WHERE user = '{player_2.name}'

                      ''')
            second_count = query.fetch_one()[0]

            #Comprobar para jugador 2
            if second_count == 0:
                query.query(f'''INSERT INTO user_stats (user,wins,loses,amount_captured,time) 
                            VALUES ('{player_2.name}',{player_2.return_win()},{player_2.return_lose()},{player_2.total_captured()},{time})
                            ''')
            else:
                query.query(f'''
                        UPDATE user_stats SET wins = wins + {player_2.return_win()}, 
                        loses = loses + {player_2.return_lose()}, 
                        amount_captured = amount_captured + {player_2.total_captured()}, 
                        time = time + {time} WHERE user = '{player_2.name}'
                        ''')
                
            #Comprobar para jugador 1
            if first_count == 0:
                query.query(f'''INSERT INTO user_stats (user,wins,loses,amount_captured,time) 
                            VALUES ('{player_1.name}',{player_1.return_win()},{player_1.return_lose()},{player_1.total_captured()},{time})
                            ''')
            else:
                query.query(f'''
                        UPDATE user_stats SET wins = wins + {player_1.return_win()}, 
                        loses = loses + {player_1.return_lose()}, 
                        amount_captured = amount_captured + {player_1.total_captured()}, 
                        time = time + {time} WHERE user = '{player_1.name}'
                        ''')                                
        except sqlite3.Error as e:
            print(e)
        finally:
            query.__del__()





