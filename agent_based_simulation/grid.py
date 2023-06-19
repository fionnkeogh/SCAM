import random
import math
import numpy as np
import scipy

class Cytokine:
    def __init__(self, ID, size, pos, color, spawnerID):
        self.ID = ID
        self.spawnerID = spawnerID
        self.size = size
        self.timer = random.randint(48, 52)
        self.max_timer = self.timer
        self.position = pos
        self.color = color
        self.diameter = 1
    
    def get_spawner(self):
        return self.spawnerID

    def get_size(self):
        return self.size

    def discrete_gaussian_kernel(self, t, n):
        return math.exp(-t) * scipy.special.iv(n, t)

    def compute_gaussian_kernal(self):
        ns = np.arange(-10, 10+1)
        step = (np.round(np.logspace(0,2.0436, num=self.max_timer, base=4),2)-1)[self.timer-1]
        y0 = self.discrete_gaussian_kernel(step, ns)
        self.diameter = len(np.nonzero(np.round(y0,2))[0])-1
        return y0

    def get_position(self):
        return self.position

    def update(self):
        self.timer = self.timer - 1
        if self.timer == 0:
            return 1
    
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