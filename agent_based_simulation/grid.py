import random
import math

class Cytokine:
    def __init__(self, ID, pos):
        self.ID = ID
        self.timer = random.randint(8, 12)
        self.max_timer = self.timer
        self.position = pos
        self.diameter = 1
    
    def get_position(self):
        return self.position

    def update():
        self.timer = self.timer - 1
        if self.timer == 0:
            pass
        else:
            self.diameter = self.diameter + 3
    
    def __str__(self):
        return f"Cytokine: {str(self.ID)} | Position: {str(self.position)}, Diameter: {str(self.diameter)}, time left: {self.timer}/{self.max_timer} |"

class Grid:
    def __init__(self, size):
        self.rows = size[0]
        self.cols = size[1]
        self.CytokineElements = list()

    def get_init_positions(self):
        positions = {}
        for y in range(math.floor(self.rows/2)):
            for x in range(math.floor(self.cols/2)):
                positions[f"({y},{x})"] = 1
        return positions

    def add_cytokine(self, pos):
        self.CytokineElements.append(Cytokine(pos))
        return self.CytokineElements[len(self.CytokineElements)-1]
    
    def get_size(self):
        return f"{self.rows}x{self.cols}"

    def __str__(self):
        return f"Grid of size {self.rows} times {self.cols}."