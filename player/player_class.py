
class Player:
    def __init__(self, player_color, name):
        self.player_color = player_color
        self.name = name
        self.moves_done = 0
        self.captured_pieces = {'rook' : 0, 'pawn': 0, 'queen':0, 'knight':0, 'bishop' : 0}
        self.player_turn = True
        self.has_won = 0
        self.has_lost = 0

    def counter_increase(self,piece):
        for name in self.captured_pieces.keys():
            if piece.name == name:
                self.captured_pieces[name] += 1

    def reset_counter(self):
        for name in self.captured_pieces.keys():
            self.captured_pieces[name] = 0
    
    def total_captured(self):
        counter = 0
        for name in self.captured_pieces.keys():
            counter += self.captured_pieces[name]
        return counter
    
    def reset_win(self):
        self.has_won = 0

    def set_win(self):
        self.has_won = 1
    
    def set_lose(self):
        self.has_lost = 1
    
    def reset_lose(self):
        self.has_lost = 0

    def return_win(self):
        return self.has_won
    
    def return_lose(self):
        return self.has_lost


