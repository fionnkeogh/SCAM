import time
import random
import math
import numpy as np
import scipy.special

class Cytokine:

    def __init__(self, id, x, y, radius = 10, timer = (20,25), loading_time = 6, hang_time = 5):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        #self.strength = strength
        self.timer = random.randint(*timer)
        self.max_timer = self.timer
        self.timer = 0
        self.loading_time = loading_time
        self.hang_time = hang_time

    def discrete_gaussian_kernel(self, t, n):
        return math.exp(-t) * scipy.special.iv(n, t)

    def compute_gaussian_kernal(self, t):
        ns = np.arange(-self.radius, self.radius+1)
        step = (np.round(np.logspace(0,2.0436, num=self.max_timer, base=4),2)-1)[t-1]
        y0 = self.discrete_gaussian_kernel(step, ns)
        #self.diameter = len(np.nonzero(np.round(y0,2))[0])-1
        return y0
    
    def compute_kernel(self, arr):
        center = round(np.median(np.arange(len(arr))))
        mat = np.zeros((len(arr), len(arr)))
        for x in range(center+1):
            for y in range(center+1):
                _x = center - x
                _y = center - y
            
                distance = math.sqrt(_x**2 + _y**2)
                if distance > center:
                    mat[x,y] = 0
                else:
                    mat[x,y] = arr[round(center-distance)]
                    mat[(len(arr)-1)-x,(len(arr)-1)-y] = arr[round(center-distance)]
                    mat[x,(len(arr)-1)-y] = arr[round(center-distance)]
                    mat[(len(arr)-1)-x,y] = arr[round(center-distance)]
        return mat

    def subtract_and_zero(self, arr, value):
        result = [max(0, element - value) for element in arr]
        return result

    def normalize_array(self, arr):
        min_val = min(arr)
        max_val = max(arr)
        if max_val == 0:
            return arr
        normalized = [(x - min_val) / (max_val - min_val) for x in arr]
        return normalized

    def compute_current_kernel(self):
        t = self.timer
        if t < (self.loading_time+self.hang_time):
            arr = self.compute_gaussian_kernal(self.max_timer-self.loading_time)
        else:
            arr = self.compute_gaussian_kernal((self.max_timer+self.hang_time)-t)
        arr = self.normalize_array(arr)
        if t < self.loading_time:
            arr = self.subtract_and_zero(arr, 1/round(self.max_timer/4)*(self.loading_time-t))
        mat = self.compute_kernel(arr)
        return mat
    
    def update(self) -> bool:
        if(self.timer < self.max_timer):
            self.timer = self.timer+1
            return True
        else:
            return False
        
    def __str__(self):
        return str(
            {
                "id": self.id,
                "x":self.x,
                "y":self.y,
                "time": self.timer,
                "neighborhood": str(self.compute_current_kernel().tolist())
            }
        )
    
    def __repr__(self):
        return str(self)