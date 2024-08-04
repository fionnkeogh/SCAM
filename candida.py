from player import Player

class Candida(Player):
    def __init__(self, strategy, generator):
        super().__init__(strategy, generator)

    def spawn(self):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """
        self.mutate_strategy()
        return Candida(self.strategy, self.generator)