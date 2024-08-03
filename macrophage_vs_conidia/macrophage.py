from player import Player

class Macrophage(Player):
    
    def __init__(self, strategy, generator):
        super().__init__(strategy, generator)
        self.type = 'macrophage'

    def get_replication_state(self, x, generator) -> bool:
        past = self.get_history(x)
        passive_count = past.count('0')
        #return True
        return True if generator.binomial(1, passive_count/len(past)) == 1 else False

