class Macrophage:
    def __init__(self, strategy, generator):
        """
        Each Macrophage has a strategy type (release or attack)
        And a small starting fitness
        """
        self.strategy = strategy
        self.fitness = 10
        self.generator = generator

    def contest(self, opponent, params):
        """
        Simulate the outcomes depending on the strategies
        """
        # both cells are aggressive --> 50:50 battle
        Fc_max, Fm_max, Ic_1, Ic_2, Im_1, Im_2, Rc, Rm, S1, S2, Pm = params
        if self.strategy == 1 and opponent.strategy == 1:
            self.fitness = self.fitness + Pm*(Fm_max - Im_2 - Rm)
            opponent.fitness = opponent.fitness + (1-Pm)*(Fc_max - Ic_2 - Rc)

        # macrophage aggressive candida less aggressive

        elif self.strategy == 1 and opponent.strategy == 0:
            self.fitness = self.fitness + Fm_max - Im_2
            opponent.fitness = opponent.fitness + 0
        elif self.strategy == 0 and opponent.strategy == 1:
            self.fitness = self.fitness + Fm_max - Im_1 - Rm - S2
            opponent.fitness = opponent.fitness + Fc_max - Ic_2

        # both less aggressive --> share the resource
        else:
            self.fitness = self.fitness + Fm_max - Im_1 - S1
            opponent.fitness = opponent.fitness + Fc_max - Ic_1
    


    def spawn(self, mutation_rate = 0.01):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """

        mutation = self.generator.binomial(1, mutation_rate) == 1
        if mutation:
            if self.strategy == 0:
                return Macrophage(1, self.generator)
            else:
                return Macrophage(0, self.generator)
        else:
            return Macrophage(self.strategy, self.generator)