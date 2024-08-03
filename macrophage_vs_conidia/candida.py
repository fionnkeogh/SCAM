from player import Player

class Candida(Player):
    
    def __init__(self, strategy, generator):
        super().__init__(strategy, generator)
        self.type = 'candida'


