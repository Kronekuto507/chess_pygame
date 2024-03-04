
class Player:
    def __init__(self, player_color, name):
        self.player_color = player_color
        self.name = name
        self.moves_done = 0
        self.captured_pieces = {'rook' : 0, 'pawn': 0, 'queen':0, 'knight':0, 'bishop' : 0}
        self.player_turn = True

    def counter_increase(self,piece):
        for name in self.captured_pieces.keys():
            if piece.name == name:
                self.captured_pieces[name] += 1

    def reset_counter(self):
        for name in self.captured_pieces.keys():
            self.captured_pieces[name] = 0

