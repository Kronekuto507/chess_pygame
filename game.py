import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT,CREMA
from classes_pieces.Piece import *
from player.player_class import Player

#1. MEJORAR EL SISTEMA DE CAPTURA CUANDO ESTA EN JAQUE
#2. SOLUCIONAR BUG AL MOVER: SI SE MUEVE CUALQUIER OTRA PIEZA AUN EN JAQUE, ESTO CAMBIA EL JUGADOR ACTUAL QUE TIENE QUE MOVER
class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
    #Aniluz
    def run(self):
        players = [Player('white','aaron'),Player('black','hector')]
        chess_board = Board(self.screen,players[0],players[1])
        chess_board.create_virtual_board()
        chess_board.generate_moves()

        while self.is_running and not chess_board.checkmate:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #Esta parte necesita ser debuggeada
                        x,y = event.pos
                        chess_board.select_piece_on_board(x,y)
                    elif event.button == 3:
                        x,y = event.pos
                        chess_board.move_piece_on_board(x,y)
                        if chess_board.checked_status == False:
                            chess_board.current_player_color = 'black' if chess_board.current_player_color == 'white' else 'white'
            self.screen.fill(CREMA)
            chess_board.draw_board()
            #Si hay una pieza seleccionada, entonces esta muestra las celdas a las que puede ir  
            for row in chess_board.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece):
                        if piece.is_selected:
                            piece.show_squares()
            
            pygame.display.update()
        pygame.quit()

        winner = 'white' if chess_board.current_player_color == 'black' else 'black'
        print(f"Winner is {winner}")

if __name__ == "__main__":
    game = Game()
    game.run()