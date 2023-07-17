import random
import math
from enum import Enum
from agent_based_simulation.directions import directions
import textwrap
import random
from enum import Enum
from agent_based_simulation.directions import directions

class AgentTypes(Enum):
    """Enumerator class for agent types"""
    DEFAULT = 0
    CANDIDA = 1
    MACROPHAGE = 2

class Agent:
    """
    Agent parent class
    Contains all the unspecific methods for movement, action selection, etc...
    """

    def __init__(self, ID, x = 0, y = 0, d = 0, size=1, color="blue", agent_type = AgentTypes.DEFAULT, bounds_x = 30, bounds_y = 30, strategy = '1010'):
        """
        Agent constructor

        Parameters:
        ID (str): The name of the agent
        x (int:): The initial position of the agent on the x-axis
        y (int): The initial position of the agent on the y-axis
        d (int): The initial direction of the agent
        size (int): The size of the agent
        color (str): The color of the agent
        agent_type (AgentTypes): The type of the agent (macrophage or candida)
        bounds_x (int):
        bounds_y (int):
        strategy (str): The strategy of the agent 
        """
        self.ID = ID
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.direction = d
        self.color = color
        self.type = agent_type
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        self.number_of_children = 0
        self.memory = int(math.log2(len(strategy)))
        self.strategy = strategy
        self.strategy_dict = self.make_dict(self.strategy)
        self.history = ''
        for i in range(self.memory):
            self.history += random.choice(['0', '1'])
        self.score = 0

    def update(self):
        """method that calls the moce method"""

        self.move()
    
    def move(self, direction = None, step = 1):
        """
        Method that moves the agent in a direction by a given number of cells on the grid.
        If not direction is given the agent will move in a random direction.
        If not step size is given the agent will move 1 cell.
        If the agent would move out of the grid it will move the opposite side of the grid.


        Parameters:
        direction (directions): The direction the agent should move (north, east, west or south)
        step (int): The number of cells the agent should move
        """
        if direction is None:
            direction = self.randomDirection()
        if direction == directions.NORTH:
            self.y_pos += step
        elif direction == directions.EAST:
            self.x_pos += step
        elif direction == directions.SOUTH:
            self.y_pos -= step
        else:
            self.x_pos -= step
        
        if self.y_pos >= self.bounds_y:
            self.y_pos = 0
        if self.x_pos >= self.bounds_x:
            self.x_pos = 0
        if self.y_pos < 0:
            self.y_pos = self.bounds_y-1
        if self.x_pos < 0:
            self.x_pos = self.bounds_x-1
        
    def __str__(self):
        """Method to print the agent object as a string"""
        agent_type = "Default"
        if self.type == AgentTypes.CANDIDA:
            agent_type = "Candida"
        elif self.type == AgentTypes.MACROPHAGE:
            agent_type = "Macrophage"
        direction = "North"
        if self.direction == directions.EAST:
            direction = "East"
        elif self.direction == directions.SOUTH:
            direction = "South"
        elif self.direction == directions.WEST:
            direction = "West"

        return f"{agent_type}-Agent {self.ID}:\t|Pos: {self.x_pos},{self.y_pos}\tFacing: {direction}\tScore: {self.score}\tStrategy: {self.strategy}\tChildren: {self.number_of_children}|"
    
    def randomDirection(self):
        """This will return a random direction in degrees."""
        return random.choice(list(directions))

    
    def randomStep(self):
        """This will return a random step length between 0 and 1, with a 0.1f stepsize."""
        return float(random.randomint(0, 10))/10
    
    def get_ID(self):
        """returns agents ID"""
        return self.ID
    
    def get_children(self):
        """returns number of agents children"""
        return self.number_of_children
    
    def add_child(self):
        """adds a child to the agents child counter"""
        self.number_of_children += 1
    
    def make_dict(self, strat):
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
        mem = int(math.log2(len(strat)))
        temp = []
        for i in range(1<<mem):
            s=bin(i)[2:]
            s='0'*(mem-len(s))+s
            temp.append(s)
        strat_dict = {temp[i]: list(strat)[i] for i in range(len(temp))}
        return strat_dict
    
    def add_history(self, event):
        """Adds an event to the agents history"""
        self.history += event
    
    def get_memory(self):
        """Returns the agents memory length"""
        return self.memory
    
    def get_strategy(self):
        """Returns the agents strategy"""
        return self.strategy

    def get_history(self, mem):
        """Returns the agents history"""
        return self.history[-mem:]
    
    def get_action(self):
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
    
    def flip(self, action):
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
    
    def point_mut(self):
        """
        This method does a point mutation in the agents strategy.
        It choses a random position in the strategy and then flips it.
        """
        index = random.randint(0, len(self.strategy)-1)
        self.strategy = self.strategy[:index] + self.flip(self.strategy[index]) + self.strategy[index + 1:]
        self.strategy_dict = self.make_dict(self.strategy)

    def incr_memory(self):
        """
        This method increases the agents memory by 1.
        To do this it doubles the strategy length by duplicating it.
        """
        self.strategy = self.strategy + self.strategy
        self.memory = self.memory + 1
        self.strategy_dict = self.make_dict(self.strategy)

    def decr_memory(self):
        """
        This method decreases the agents memory by 1.
        To do this it splits the strategy in hald and randomly choses one half to keep.
        """
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
            self.strategy_dict = self.make_dict(self.strategy)

    def random_mut(self):
        """This method randomly executes one of the 3 possible mutation."""
        mutations = ['point_mut', 'incr_memory', 'decr_memory']
        random_mutation = random.choice(mutations)
        mutation_function = getattr(self, random_mutation)
        mutation_function()

    def add_score(self, score):
        """This method modifies the agents score by adding a positive or negative value to it."""
        self.score += score

    def reset_score(self):
        """This emthod resets the agents score to zero."""
        self.score = 0

