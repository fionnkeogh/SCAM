import time
import math
import random

class Player:
    def __init__(self, id, strategy = "1010"):
        self.id: int = id
        self.strategy: str = strategy
        self.memory: int = int(math.log2(len(self.strategy)))
        self.score: int = 0
        self.history: str = ""
        for i in range(self.memory):
            self.history += random.choice(["0", "1"])
        self.strategy_dict: dict[str, str] = self.make_strategy_dict(self.strategy, self.memory)
    
    def make_strategy_dict(self, strategy, memory) -> dict[str, str]:
        """
        This method creates a look-up dict for a given strategy 

        Parameters:
        strat (str): The input strategy, example: "1001"

        Returns:
        dict: A dictionary containing possible pasts as keys and the corresponding action as value
              example:
              {
              "00": "1"
              "01": "0"
              "10": "0"
              "11": "1"
              }
        """
        temp = []
        for i in range(1<<memory):
            s=bin(i)[2:]
            s="0"*(memory-len(s))+s
            temp.append(s)
        strategy_dict = {temp[i]: list(strategy)[i] for i in range(len(temp))}
        return strategy_dict
    
    def add_history(self, event) -> None:
        """Adds an event to the agents history"""
        self.history += event
    
    def get_memory(self) -> int:
        """Returns the agents memory length"""
        return self.memory
    
    def get_strategy(self) -> str:
        """Returns the agents strategy"""
        return self.strategy

    def get_history(self, mem) -> str:
        """Returns the agents history"""
        return self.history[-mem:]
    
    def get_action(self) -> str:
        """
        This method determines the next action for the agent to take.
        To do that it looks up the last events in its strategy dictionary.
        Due to an increase in memory by mutation it is possible that the agents history is shorter than its memory.
        In that case it will temporarily reduce its memory by 1 and then randomly use either the first or second half of its strategy.
        If its history is still to short it will repeat the process until it is long enough.

        Returns:
        str: The action which will be taken
        """
        mem = self.get_memory()
        past = self.get_history(mem)
        if len(past) < mem:
            while  len(past) < mem:
                mem -= 1
            past = self.get_history(mem)
            diff = self.get_memory() - mem
            parts_no = 2**diff
            width = len(self.get_strategy()) // parts_no
            parts = textwrap.wrap(self.get_strategy(), width)
            strat = random.choice(parts)
            strat_dict = self.make_dict(strat)
            return strat_dict[past]
        else:
            return self.strategy_dict.get(past)
    
    def flip(self, action) -> str:
        """
        This method inverts a given action.
        If given "1" as input it will return "0" and vice versa

        Parameters:
        action (str): The action to be flipped

        Returns:
        str: The flipped action
        """
        if action == '1':
            return '0'
        else:
            return '1'
    
    def point_mut(self) -> None:
        """
        This method does a point mutation in the agents strategy.
        It choses a random position in the strategy and then flips it.
        """
        index = random.randint(0, len(self.strategy)-1)
        self.strategy = self.strategy[:index] + self.flip(self.strategy[index]) + self.strategy[index + 1:]
        self.strategy_dict = self.make_dict(self.strategy)

    def increase_memory(self) -> None:
        """
        This method increases the agents memory by 1.
        To do this it doubles the strategy length by duplicating it.
        """
        self.strategy = self.strategy + self.strategy
        self.memory = self.memory + 1
        self.strategy_dict = self.make_dict(self.strategy)

    def decrease_memory(self) -> None:
        """
        This method decreases the agents memory by 1.
        To do this it splits the strategy in hald and randomly choses one half to keep.
        """
        if len(self.strategy) >= 4:
            index = int(len(self.strategy) / 2)
            strat_a = self.strategy[:index]
            strat_b = self.strategy[index:]
            self.strategy = random.choice([strat_a, strat_b])
            self.memory = self.memory - 1
            self.strategy_dict = self.make_dict(self.strategy)

    def random_mutation(self) -> None:
        """This method randomly executes one of the 3 possible mutation."""
        mutations = ['point_mut', 'incr_memory', 'decr_memory']
        random_mutation = random.choice(mutations)
        mutation_function = getattr(self, random_mutation)
        mutation_function()

    def add_score(self, score) -> None:
        """This method modifies the agents score by adding a positive or negative value to it."""
        self.score += score

    def reset_score(self) -> None:
        """This emthod resets the agents score to zero."""
        self.score = 0