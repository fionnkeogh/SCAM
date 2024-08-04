class Bird:
    def __init__(self, strategy, generator):
        """
        Each bird has a strategy type (hawk or dove)
        And a small starting fitness
        """
        self.strategy = strategy
        self.fitness = 10
        self.generator = generator

    def contest(self, opponent, v, c):
        """
        Simulate the outcomes depending on the strategies
        """
        # both hawks --> 50:50 battle

        if self.strategy == opponent.strategy == "hawk":
            if self.generator.binomial(1, 0.5) == 1:
                self.fitness = self.fitness + v
                opponent.fitness = opponent.fitness - c
            else:
                self.fitness = self.fitness - c
                opponent.fitness = opponent.fitness + v

        # hawk meets dove

        elif self.strategy == "hawk" != opponent.strategy:
            self.fitness = self.fitness + v
            opponent.fitness = opponent.fitness
        elif self.strategy == "dove" != opponent.strategy:
            self.fitness = self.fitness
            opponent.fitness = opponent.fitness + v

        # both doves --> share the resource

        else:
            self.fitness = self.fitness + v/2
            opponent.fitness = opponent.fitness + v/2

    def spawn(self):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """

        mutation = self.generator.binomial(1, 0.001) == 1
        if mutation:
            if self.strategy == "dove":
                return Bird("hawk", self.generator)
            else:
                return Bird("dove", self.generator)
        else:
            return Bird(self.strategy, self.generator)