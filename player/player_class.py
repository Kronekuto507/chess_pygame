
class Player:
    def __init__(self, player_color, name):
        self.player_color = player_color
        self.name = name
        self.moves_done = 0
        self.captured_pieces = []
        self.player_turn = True
    def add_caputred(self, piece):
        self.captured_pieces.append(piece)

