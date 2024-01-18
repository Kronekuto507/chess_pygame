
class Player:
    def __init__(self, player_color):
        self.player_color = player_color
        self.is_checkmated = False
        self.is_checked = False
        self.captured_pieces = []
        self.player_turn = True
    def add_caputred(self, piece):
        self.captured_pieces.append(piece)

