from player import Player
import math

class Macrophage(Player):
    def __init__(self, strategy, generator):
        super().__init__(strategy, generator)
        
    def contest(self, opponent, params):
        """
        Simulate the outcomes depending on the strategies
        """
        Fc_max, Fm_max, Ic_1, Ic_2, Im_1, Im_2, Rc, Rm, S1, S2, Pm = params
        
        action = self.get_action()
        action_opponent = opponent.get_action()

        if action == action_opponent == '1':
            self.fitness = self.fitness + Pm*(Fm_max - Im_2 - Rm)
            opponent.fitness = opponent.fitness + (1-Pm)*(Fc_max - Ic_2 - Rc)
        # macrophage aggressive candida less aggressive
        elif action == '1' != action_opponent:
            self.fitness = self.fitness + Fm_max - Im_2
            opponent.fitness = opponent.fitness + 0
        elif action == '0' != action_opponent:
            self.fitness = self.fitness + Fm_max - Im_1 - Rm - S2
            opponent.fitness = opponent.fitness + Fc_max - Ic_2
        # both less aggressive --> share the resource
        else:
            self.fitness = self.fitness + Fm_max - Im_1 - S1
            opponent.fitness = opponent.fitness + Fc_max - Ic_1
    
    def spawn(self):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """
        self.mutate_strategy()
        return Macrophage(self.strategy, self.generator)