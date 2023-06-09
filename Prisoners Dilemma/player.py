import math
import random

class Player():

    def __init__(self, name, strategy):
        self.name = name
        self.memory = int(math.log2(len(strategy)))
        self.strategy = strategy
        self.make_dict()
        self.history = ''
    
    def make_dict(self):
        temp = []
        for i in range(1<<self.memory):
            s=bin(i)[2:]
            s='0'*(self.memory-len(s))+s
            temp.append(s)
        self.strategy_dict = {temp[i]: list(self.strategy)[i] for i in range(len(temp))}
    
    def add_history(self, event):
        self.history += event

    def get_history(self):
        return self.history[-self.memory:]
    
    def get_action(self):
        past = self.get_history()
        if len(past) < self.memory:
            return random.choice(['0', '1'])
        else:         
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
        self.strategy = self.strategy + self.strategy
        self.memory = self.memory + 1
        self.make_dict()

    def decr_memory(self):
        index = len(self.strategy) / 2
        strat_a = self.strategy[:index]
        strat_b = self.strategy[index:]
        r = random.randint(0,1)
        if r == 0:
            self.strategy = strat_a
        else:
            self.strategy = strat_b
        self.memory = self.memory - 1