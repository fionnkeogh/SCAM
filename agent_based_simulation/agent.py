import random
from enum import Enum
from agent_based_simulation.directions import directions

class AgentTypes(Enum):
    DEFAULT = 0
    CANDIDA = 1
    MACROPHAGE = 2

class Agent:
    def __init__(self, ID, brain, x = 0, y = 0, d = 0, size=1, color="blue", agent_type = AgentTypes.DEFAULT, bounds_x = 30, bounds_y = 30):
        self.ID = ID
        self.brain = brain
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.direction = d
        self.color = color
        self.type = agent_type
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
    
    def update(self):
        self.move()
    
    def move(self, direction = None, step = 1):
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

        return f"{agent_type}-Agent {self.ID}:\t|Pos: {self.x_pos},{self.y_pos}\tFacing: {direction}\tScore: {self.brain.score}\tStrategy: {self.brain.strategy}|"
    
    def randomDirection(self):
        """This will return a random direction in degrees."""
        return random.choice(list(directions))

    
    def randomStep(self):
        """This will return a random step length between 0 and 1, with a 0.1f stepsize."""
        return float(random.randomint(0, 10))/10
