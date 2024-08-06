import math

class Player:
    def __init__(self, strategy, generator):
        """
        Each player has a strategy type (1 or 0)
        """
        self.strategy = strategy
        self.fitness = 10
        self.generator = generator
        if len(self.strategy) == 1:
            self.memory = 1
        else:
            self.memory = int(math.log2(len(strategy)))
        self.dict = {}
        self.make_dict()
        self.history = ''
        for i in range(self.memory):
            self.history += generator.choice(['0', '1'])

    def make_dict(self):
        temp = []
        for i in range(1<<self.memory):
            s=bin(i)[2:]
            s='0'*(self.memory-len(s))+s
            temp.append(s)
        self.strategy_dict = {temp[i]: list(self.strategy)[i%len(self.strategy)] for i in range(len(temp))}

    def add_history(self, event):
        self.history += event

    def get_history(self, x):
        return self.history[-x:]
    
    def get_action(self):
        past = str(self.get_history(self.memory))
        return self.strategy_dict.get(past)

    def flip(self, action):
        if action == '1':
            return '0'
        else:
            return '1'

    def mutate_strategy(self, mutation_rate = 0.001):
        mutation = self.generator.binomial(1, mutation_rate * len(self.strategy)) == 1
        if mutation:
            index = self.generator.integers(low = 0, high = len(self.strategy), size = 1)[0]
            self.strategy = self.strategy[:index] + self.flip(self.strategy[index]) + self.strategy[index + 1:]
            self.make_dict()

    def spawn(self):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """
        self.mutate_strategy()
        return Player(self.strategy, self.generator)