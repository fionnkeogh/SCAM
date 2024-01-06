import random
import numpy as np

class Grid():
    def __init__(self, width: int, height: int):
        self.agents: np.array = np.zeros((height, width))
        self.cytokines: np.array = np.zeros((height, width))
        self.gradient_strength: np.array = np.full((height, width, 2), [0,0])
        self.agent_position_dict: dict[int, list[[int,int]]] = dict()
        self.possible_spawns: dict[str, (int,int)] = dict()
    
    def update_spawns(self, size = 1):
        height, width = np.shape(self.agents)
        self.possible_spawns = dict()
        for x in range(0,width-1, size):
            for y in range(0,height-1, size):
                if self.agents[y, x] == 0:
                    self.possible_spawns[str([x,y])] = (x,y)

    def get_spawn_position(self, size):
        pos = random.choice(list(self.possible_spawns.keys()))
        x,y = self.possible_spawns.get(pos)
        self.possible_spawns.pop(pos)
        return (x,y)

    def get_tile(self, x: int, y: int) -> list:
        agent = self.agents[y, x]
        cytokine = self.cytokines[y, x]
        gradient = self.gradient_strength[y, x]

        return [agent, cytokine, gradient]

    def set_cytokine(self, x: int, y: int, id: int) -> None:
        self.cytokines[y, x] = id
    
    def get_cytokine(self, id: int) -> tuple:
        height, width = np.shape(self.cytokines)
        for x in range(width):
            for y in range(height):
                if self.cytokines[y, x] == id:
                    return (x,y)
        return (-1,-1)

    def set_gradient(self, x: int, y: int, strength: float, id: int) -> None:
        if strength > self.gradient_strength[y, x][1]:
            self.gradient_strength[y, x] = [id, strength]
    
    def set_agent(self, x: int, y: int, size: int, id: int) -> None:
        old_pos = self.agent_position_dict.get(id)
        print(old_pos)
        if old_pos != None:
            for pos in old_pos:
                self.agents[pos[0], pos[1]] = 0
        x_size = x+(size-1) if x+(size-1) < self.get_size()[1] else 0
        y_size = y+(size-1) if y+(size-1) < self.get_size()[0] else 0
        self.agents[y, x] = id
        self.agents[y, x_size] = id
        self.agents[y_size, x] = id
        self.agents[y_size, x_size] = id

        self.agent_position_dict[id] = [[y, x],[y, x_size],[y_size, x],[y_size, x_size]]

    def get_direction(self, x: int, y: int) -> int:
        arr = self.gradient_strength[y, x]
        strength = arr[1]
        cytokine_id = arr[0]
        if strength > 0:
            return cytokine_id
        else:
            return 0
    
    def get_size(self) -> tuple:
        return tuple(np.shape(self.cytokines))

    def get_possible_directions(self, x: int, y: int, size: int) -> list[str]:
        directions: list[str] = []
        up = y-1 if y-1 > 0 else self.get_size()[0]-1
        down = y+(size-1)+1 if y+(size-1)+1 < self.get_size()[0] else 0
        left = x-1 if x-1 > 0 else self.get_size()[1]-1
        right = x+(size-1)+1 if x+(size-1)+1 < self.get_size()[1] else 0

        if self.agents[up, x] == 0 and self.agents[up, (x+(size-1) if x+(size-1) < self.get_size()[1] else 0)] == 0:
            directions.append("UP")
        if self.agents[down, x] == 0 and self.agents[down, (x+(size-1) if x+(size-1) < self.get_size()[1] else 0)] == 0:
            directions.append("DOWN")
        if self.agents[y, left] == 0 and self.agents[y+(size-1) if y+(size-1) < self.get_size()[0] else 0, left] == 0:
            directions.append("LEFT")
        if self.agents[y, right] == 0 and self.agents[y+(size-1) if y+(size-1) < self.get_size()[0] else 0, right] == 0:
            directions.append("RIGHT")
        return directions



        # [   [      0.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [1000003.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0. 1000006.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0. 1000007.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [1000000. 1000000.       0.       0.       0. 1000004.       0.       0.    0.       0.]
        #     [1000000. 1000000.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [1000002. 1000002. 1000005.       0.       0.       0. 1000001. 1000001.    0.       0.]
        #     [1000002. 1000002.       0.       0.       0.       0. 1000001. 1000001.    0.       0.]]

        # [   [      0.       0.       0.       0.       0.       0. 1000001. 1000001.    0.       0.]
        #     [      0.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [1000003.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0. 1000006.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0. 1000007.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [      0.       0.       0.       0.       0. 1000004.       0.       0.    0.       0.]
        #     [1000000. 1000000.       0.       0.       0.       0.       0.       0.    0.       0.]
        #     [1000002.       0. 1000005.       0.       0.       0.       0.       0.    0. 1000002.]
        #     [1000002.       0.       0.       0.       0.       0. 1000001. 1000001.    0. 1000002.]]