import random

from python.player import Player
from python.grid import Grid

class Macrophage(Player):
    
    def __init__(self, id, x, y, grid: Grid, size = 2, step_size = 1):
        super().__init__(id)
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.step_size: int = step_size
        self.children: list[Macrophage] = []
        grid.set_agent(self.x, self.y, self.size, self.id)
    
    def update(self, grid: Grid) -> None:
        direction: str = self.determine_direction(grid)
        self.move(direction, grid)
        grid.set_agent(self.x, self.y, self.size, self.id)

    def determine_direction(self, grid: Grid) -> str:
        cytokine_id: int = grid.get_direction(self.x, self.y)
        x,y = self.x, self.y
        if cytokine_id != 0:
            x, y = grid.get_cytokine(cytokine_id)
        x_distance: int = self.x - x
        y_distance: int = self.y - y
        directions = grid.get_possible_directions(self.x, self.y, self.size)
        if x_distance == 0 and y_distance == 0:
            return random.choice(directions)
        direction_dict = {directions[i]: 0 for i in range(len(directions))}
        if len(direction_dict.keys()) == 0:
            return "NONE"

        for key in direction_dict.keys():
            if key == "UP":
                direction_dict[key] = grid.get_tile(x, y-1)[2][1]
            if key == "DOWN":
                direction_dict[key] = grid.get_tile(x, y+1)[2][1]
            if key == "LEFT":
                direction_dict[key] = grid.get_tile(x-1, y)[2][1]
            if key == "RIGHT":
                direction_dict[key] = grid.get_tile(x+1, y)[2][1]
        
        sorted_dict = dict(sorted(direction_dict.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_dict.keys())[0]

    def move(self, direction: str, grid: Grid) -> None:
        y, x = grid.get_size()
        if direction == "UP":
            self.y += self.step_size
        elif direction == "LEFT":
            self.x += self.step_size
        elif direction == "DOWN":
            self.y -= self.step_size
        elif direction == "RIGHT":
            self.x -= self.step_size
        
        if self.y >= y:
            self.y = 0
        if self.x >= x:
            self.x = 0
        if self.y < 0:
            self.y = y-1
        if self.x < 0:
            self.x = x-1
        
        grid.set_agent(self.x, self.y, self.size, self.id)

    def get_children(self) -> list:
        """returns list of agents children"""
        return self.children
    
    def add_child(self, macrophage) -> None:
        """adds a child to the agents child counter"""
        self.children.append(macrophage)

    def __str__(self) -> str:
        return str(
                {
                    "id": self.id,
                    "type": "Macrophage",
                    "x":self.x,
                    "y":self.y,
                    "score": self.score,
                    "strategy": self.strategy,
                    "memory": self.memory,
                    "history": self.history,
                    "children": str(self.children)
                }
            )
    
    def __repr__(self) -> str:
        return str(self)