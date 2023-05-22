from macrophage_vs_conidia.player import Player

class Candida(Player):
    
    def __init__(self, name, strategy):
        super().__init__(name, strategy)
        self.type = 'candida'


