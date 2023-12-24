
black_pieces = []
white_pieces = []
class Player:
    def __init__(self, player_color, captured_pieces):
        self.player_color = player_color
        self.is_checkmated = False
        self.is_checked = False
        self.captured_pieces = captured_pieces
        self.player_turn = True
    def move_piece(self):
        pass
    def set_player_turn(self, color):
        pass

