import random
from directions import directions

class Agent:
    def __init__(self, ID, x = 0, y = 0, d = 0, color="blue", bounds_x = 30, bounds_y = 30):
        self.ID = ID
        self.x_pos = x
        self.y_pos = y
        self.direction = d
        self.color = color
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
    
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
        

    
    def randomDirection(self):
        """This will return a random direction in degrees."""
        return random.choice(list(directions))

    
    def randomStep(self):
        """This will return a random step length between 0 and 1, with a 0.1f stepsize."""
        return float(random.randomint(0, 10))/10
