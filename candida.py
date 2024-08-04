class Candida:
    def __init__(self, strategy, generator):
        """
        Each Candida has a strategy type (less aggressive or aggressive)
        And a small starting fitness
        """
        self.strategy = strategy
        self.fitness = 10
        self.generator = generator

    def spawn(self, mutation_rate = 0.01):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """

        mutation = self.generator.binomial(1, mutation_rate) == 1
        if mutation:
            if self.strategy == 1:
                return Candida(0, self.generator)
            else:
                return Candida(1, self.generator)
        else:
            return Candida(self.strategy, self.generator)