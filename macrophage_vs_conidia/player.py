import math
import random

class Player():

    def __init__(self, strategy, generator):
        # 0 = passiv, 1 = aggressiv
        self.memory = int(math.log2(len(strategy)))
        self.strategy = strategy
        self.make_dict()
        self.history = ''
        for i in range(self.memory):
            self.history += generator.choice(['0', '1'])
        self.score = 0
    
    def make_dict(self):
        temp = []
        for i in range(1<<self.memory):
            s=bin(i)[2:]
            s='0'*(self.memory-len(s))+s
            temp.append(s)
        self.strategy_dict = {temp[i]: list(self.strategy)[i] for i in range(len(temp))}
    
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
    
    def point_mut(self):
        index = random.randint(0, len(self.strategy)-1)
        self.strategy = self.strategy[:index] + self.flip(self.strategy[index]) + self.strategy[index + 1:]
        self.make_dict()

    def incr_memory(self):
        if len(self.strategy) <= 8:
            self.strategy = self.strategy + self.strategy
            self.memory = self.memory + 1
            self.make_dict()
        else:
            pass

    def decr_memory(self):
        if len(self.strategy) >= 4:
            index = int(len(self.strategy) / 2)
            strat_a = self.strategy[:index]
            strat_b = self.strategy[index:]
            r = random.randint(0,1)
            if r == 0:
                self.strategy = strat_a
            else:
                self.strategy = strat_b
            self.memory = self.memory - 1
            self.make_dict()

    def random_mut(self):
        mutations = ['point_mut', 'incr_memory', 'decr_memory']
        random_mutation = random.choice(mutations)
        mutation_function = getattr(self, random_mutation)
        mutation_function()

    def mutate(self, rate_point, rate_mem, generator):
        mod = len(self.strategy)
        if generator.binomial(1, rate_point*mod) == 1:
            self.point_mut()
        elif generator.binomial(1, rate_mem*mod) == 1:
            self.incr_memory()
        elif generator.binomial(1, rate_mem*mod) == 1:
            self.decr_memory()
        else:
            pass

    def add_score(self, score):
        self.score += score

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score
    
    def get_strategy(self):
        return self.strategy