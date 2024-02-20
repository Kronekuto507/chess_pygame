import pygame
from pygame.locals import *
from board.board_template import *
from board.constants import WIDTH,HEIGHT
from classes_pieces.Piece import *
from player.player_class import Player

#Se han solucionado la mayoría de las cosas. Ahora se debe de detectar si está en jaquemate correctamente. 
#Enroque largo no funciona y el rey aun cuando hayan casillas en las que no este en jaque y pueda moverse este no se mueve a ellas
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
        clock = pygame.time.Clock()
        while self.is_running:
            
            self.screen.fill(VERDE)
            chess_board.draw_board()         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #Esta parte necesita ser debuggeada
                        x,y = event.pos
                        chess_board.select_piece_on_board(x,y)
                        chess_board.internal_logic_of_selection()
                    elif event.button == 3:
                        x,y = event.pos
                        chess_board.move_piece_on_board(x,y)

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
                break
            
            #Si hay una pieza seleccionada, entonces esta muestra las celdas a las que puede ir  
            for row in chess_board.virtual_board:
                for piece in row:
                    if isinstance(piece,Piece):
                        if piece.is_selected:
                            piece.show_squares(chess_board)
            
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

        winner = 'white' if chess_board.current_player_color == 'black' else 'black'
        print(f"Winner is {winner}")

if __name__ == "__main__":
    game = Game()
    game.run()