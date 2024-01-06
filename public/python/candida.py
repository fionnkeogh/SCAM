from python.player import Player
from python.grid import Grid

class Candida(Player):

    def __init__(self, id, x, y, grid: Grid, size = 1):
        super().__init__(id)
        self.x: int = x
        self.y: int = y
        self.size: int = size
        grid.set_agent(self.x, self.y, self.size, self.id)

    def update(self) -> None:
        pass

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
                    "history": self.history
                }
            )
    
    def __repr__(self) -> str:
        return str(self)