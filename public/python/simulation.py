import random
import time
import math
import numpy as np
import scipy.special
#from python.grid import Grid
#from cytokine import Cytokine
#from macrophage import Macrophage
#from candida import Candida

class Player():
    def __init__(self, id, suf, size):
        self.id = str(suf) + ':' + str(id)
        self.size = size
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y
    
class Macrophage(Player):
    def __init__(self, id):
        super().__init__(id, 'M', 2)
        self.cool_down = 0
    
    def __str__(self) -> str:
        return str(
                {
                    "id": self.id,
                    "type": "Macrophage",
                    "x":self.x,
                    "y":self.y
                    # "score": self.score,
                    # "strategy": self.strategy,
                    # "memory": self.memory,
                    # "history": self.history,
                    # "children": str(self.children)
                }
            )
    
    def __repr__(self) -> str:
        return str(self)

class Candida(Player):
    def __init__(self, id):
        super().__init__(id, 'C', 1)
    
    def __str__(self) -> str:
        return str(
                {
                    "id": self.id,
                    "type": "Candida",
                    "x":self.x,
                    "y":self.y
                    # "score": self.score,
                    # "strategy": self.strategy,
                    # "memory": self.memory,
                    # "history": self.history
                }
            )
    
    def __repr__(self) -> str:
        return str(self)

class Cytokine():
    def __init__(self, id, x, y, radius = 5, timer = (20,25), loading_time = 6, hang_time = 5):
        self.id = 'Z:' + str(id)
        self.x = x
        self.y = y
        self.radius = radius
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

    def get_position(self):
        return (self.y, self.x)
    
    def __str__(self):
        return str(
            {
                "id": self.id,
                "x":self.x,
                "y":self.y,
                "time": self.timer
            }
        )
    
    def __repr__(self):
        return str(self)

class Simulation():
    """This class handles the actual simulation"""
    def __init__(self, width: int = 10, height: int = 10, num_m: int = 5, num_c: int = 3, max_steps: int = 100, seed: int = 1234):
        """
        Constructor

        Parameters:
        width (int): dimensions of the grid
        height (int): dimensions of the grid
        num_path (int): number of pathogens
        num_phages (int): number of macrophages
        seed (int): for reproducablility
        """
        random.seed(seed)
        self.max_steps = max_steps
        self.id_count = 0
        self.grid: np.array = np.full((height, width), str(), dtype=np.dtype('U100'))
        self.macrophages: dict = dict()
        self.candidae: dict() = dict()
        self.cytokines: dict() = dict()
        self.cytokine_grid: np.array = np.full((height, width, 2), ['',0])
        for n in range(num_m):
            m = Macrophage(self.id_count)
            self.macrophages[m.id] = m
            self.id_count += 1
        for n in range(num_c):
            c = Candida(self.id_count)
            self.candidae[c.id] = c
            self.id_count += 1
        self.init_agents()
        self.step = 0

    def get_max_steps(self):
        return self.max_steps
    
    def get_current_step(self):
        return self.step

    def get_grid_size(self):
        return str({'x':self.grid.shape[1], 'y':self.grid.shape[0]})

    def update_spawns(self, size = 1):
        height, width = np.shape(self.grid)
        possible_spawns = dict()
        for x in range(0,width-1, size):
            for y in range(0,height-1, size):
                if self.grid[y, x] == '':
                    possible_spawns[str([x,y])] = (x,y)
        return possible_spawns

    def spawn_agent(self, agent: Player, possible_spawns: dict[str, (int,int)]):
        pos = random.choice(list(possible_spawns.keys()))
        x,y = possible_spawns.pop(pos)
        for x_off in range(0, agent.size):
            for y_off in range(0, agent.size):
                self.grid[y + y_off, x + x_off] = agent.id
        agent.set_position(x,y)
        return possible_spawns

    def init_agents(self):
        possible_spawns: dict[str, (int,int)] = self.update_spawns(2)
        for m in self.macrophages.keys():
            possible_spawns = self.spawn_agent(self.macrophages[m], possible_spawns)
        possible_spawns: dict[str, (int,int)] = self.update_spawns(1)
        #print(possible_spawns)
        for c in self.candidae.keys():
            possible_spawns = self.spawn_agent(self.candidae[c], possible_spawns)
    
    def get_cytokine(self, x: int, y: int) -> int:
        arr = self.cytokine_grid[y, x]
        strength = float(arr[1])
        cytokine_id = arr[0]
        if strength > 0:
            return cytokine_id
        else:
            return ''

    def get_cytokine_position(self, id):
        return self.cytokines.get(id).get_position()

    def get_tile(self, x: int, y: int) -> list:
        agent = None
        #print(self.grid[y,x])
        x = x if x < np.shape(self.grid)[1] and x >= 0 else (0 if x < np.shape(self.grid)[1] else np.shape(self.grid)[1]-1)
        y = y if y < np.shape(self.grid)[0] and y >= 0 else (0 if y < np.shape(self.grid)[0] else np.shape(self.grid)[0]-1)
        if len(self.grid[y, x]) > 0 and self.grid[y, x][0] == 'M':
            agent = self.macrophages[self.grid[y, x]]
        elif len(self.grid[y, x]) > 0 and self.grid[y, x][0] == 'C':
            agent = self.candidae[self.grid[y, x]]
        cytokine = None
        gradient = self.cytokine_grid[y, x]
        if gradient[0] != '':
            cytokine = self.cytokines.get(gradient[0])

        return [agent, cytokine, gradient]

    def get_direction_for_agent(self, agent: Macrophage):
        up_y = agent.y - 1 if agent.y-1 >= 0 else self.grid.shape[0]-2
        down_y = agent.y + agent.size if agent.y + agent.size < self.grid.shape[0] else 0
        left_x = agent.x - 1 if agent.x-1 >= 0 else self.grid.shape[1]-2
        right_x = agent.x + agent.size if agent.x + agent.size < self.grid.shape[1] else 0
        
        x,y = agent.x, agent.y
        cytokine_id = self.get_cytokine(x, y)
        
        if cytokine_id != '':
            y, x = self.get_cytokine_position(cytokine_id)
        x_distance: int = x - agent.x
        y_distance: int = y - agent.y

        directions: list[str] = []

        # move_up
        if self.grid[up_y, agent.x] == '' and self.grid[up_y, agent.x+(agent.size-1)] == '':
            directions.append("UP")
        if self.grid[down_y, agent.x] == '' and self.grid[down_y, agent.x+(agent.size-1)] == '':
            directions.append("DOWN")
        if self.grid[agent.y, left_x] == '' and self.grid[agent.y+(agent.size-1), left_x] == '':
            directions.append("LEFT")
        if self.grid[agent.y, right_x] == '' and self.grid[agent.y+(agent.size-1), right_x] == '':
            directions.append("RIGHT")
        
        direction_dict = {directions[i]: 0 for i in range(len(directions))}
        if len(direction_dict.keys()) == 0:
            return "NONE"

        if x_distance == 0 and y_distance == 0:
            return random.choice(directions)

        direction_dict = {directions[i]: 0 for i in range(len(directions))}
        if len(direction_dict.keys()) == 0:
            return "NONE"
        
        for key in direction_dict.keys():
            if key == "UP":
                direction_dict[key] = self.get_tile(x, y-1)[2][1]
            if key == "DOWN":
                direction_dict[key] = self.get_tile(x, y+1)[2][1]
            if key == "LEFT":
                direction_dict[key] = self.get_tile(x-1, y)[2][1]
            if key == "RIGHT":
                direction_dict[key] = self.get_tile(x+1, y)[2][1]
        
        sorted_dict = dict(sorted(direction_dict.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_dict.keys())[0]
    
    def move_agent(self, agent: Player, direction: str):
        x = agent.x
        y = agent.y
        for x_off in range(0, agent.size):
            for y_off in range(0, agent.size):
                self.grid[y + y_off, x + x_off] = ''
        match direction:
            case "UP":
                y = y - 1 if y - 1 >= 0 else self.grid.shape[0]-2
            case "DOWN":
                y = y + 1 if y + agent.size < self.grid.shape[0] else 0
            case "LEFT":
                x = x - 1 if x - 1 >= 0 else self.grid.shape[1]-2
            case "RIGHT":
                x = x + 1 if x + agent.size < self.grid.shape[1] else 0
            case _:
                pass
        for x_off in range(0, agent.size):
            for y_off in range(0, agent.size):
                self.grid[y + y_off, x + x_off] = agent.id
        agent.set_position(x, y)

    def spawn_cytokine(self, pos):
        cytokine = Cytokine(self.id_count, pos[1], pos[0], radius=5)
        self.id_count += 1
        self.cytokines[cytokine.id] = cytokine

    def update_cytokines(self):
        if len(self.cytokines.keys()) == 0:
            return
        else:
            old_cytokine_grid = np.copy(self.cytokine_grid)
            proto = np.zeros(len(self.cytokines.keys()))
            self.cytokine_grid_all = np.zeros((old_cytokine_grid.shape[0], old_cytokine_grid.shape[1], len(self.cytokines.keys())))
            # for x in range(0,np.shape(self.cytokine_grid_all)[1]):
            #     for y in range(0,np.shape(self.cytokine_grid_all)[0]):
            #         self.cytokine_grid_all[y,x] = np.zeros(len(self.cytokines.keys()))
            self.cytokine_grid = np.full(old_cytokine_grid.shape, ['', 0])
            #print(self.cytokines.keys())
            to_pop = list()
            index = 0
            for i in self.cytokines.keys():
                cytokine = self.cytokines[i]
                firing = cytokine.update()
                if firing == False:
                    to_pop.append(i)
                else:
                    current_kernel = cytokine.compute_current_kernel()
                    y, x = cytokine.get_position()
                    for y_kern in range(2*cytokine.radius+1):
                        for x_kern in range(2*cytokine.radius+1):
                            _y = cytokine.radius - y_kern
                            _x = cytokine.radius - x_kern
                            if x + _x >= 0 and x + _x < self.grid.shape[1]:
                                if y + _y >= 0 and y + _y < self.grid.shape[0]:
                                    self.cytokine_grid_all[y + _y, x + _x, index] = current_kernel[cytokine.radius + _y, cytokine.radius + _x]
                index = index + 1
            for x in range(0,np.shape(self.cytokine_grid_all)[1]):
                for y in range(0,np.shape(self.cytokine_grid_all)[0]):
                    max_index = np.argmax(self.cytokine_grid_all[y,x])
                    self.cytokine_grid[y,x] = [list(self.cytokines.keys())[max_index], self.cytokine_grid_all[y,x, max_index]]
            for i in to_pop:
                self.cytokines.pop(i)

    def check_for_players(self, agent:Player):
        up_y = agent.y - 1 if agent.y-1 >= 0 else self.grid.shape[0]-1
        down_y = agent.y + agent.size if agent.y + agent.size < self.grid.shape[0] else 0
        left_x = agent.x - 1 if agent.x-1 >= 0 else self.grid.shape[1]-1
        right_x = agent.x + agent.size if agent.x + agent.size < self.grid.shape[1] else 0
        
        x,y = agent.x, agent.y

        possible_games = list()
        if len(self.grid[up_y,x]) > 0 and self.grid[up_y,x][0] == 'C':
            possible_games.append((self.grid[up_y,x], [y,x]))
        if len(self.grid[up_y,x+1]) > 0 and self.grid[up_y,x+1][0] == 'C':
            possible_games.append((self.grid[up_y,x+1], [y,x+1]))
        if len(self.grid[down_y,x]) > 0 and self.grid[down_y,x][0] == 'C':
            possible_games.append((self.grid[down_y,x], [y+1, x]))
        if len(self.grid[down_y,x+1]) > 0 and self.grid[down_y,x+1][0] == 'C':
            possible_games.append((self.grid[down_y,x+1], [y+1, x+1]))
        if len(self.grid[y,left_x]) > 0 and self.grid[y,left_x][0] == 'C':
            possible_games.append((self.grid[y,left_x], [y, x]))
        if len(self.grid[y+1,left_x]) > 0 and self.grid[y+1,left_x][0] == 'C':
            possible_games.append((self.grid[y+1,left_x], [y+1, x]))
        if len(self.grid[y,right_x]) > 0 and self.grid[y,right_x][0] == 'C':
            possible_games.append((self.grid[y,right_x], [y, x+1]))
        if len(self.grid[y+1,right_x]) > 0 and self.grid[y+1,right_x][0] == 'C':
            possible_games.append((self.grid[y+1,right_x], [y+1, x+1]))
        return possible_games

    def run_step(self):
        self.update_cytokines()
        for m in self.macrophages.keys():
            #print(m)
            direction = self.get_direction_for_agent(self.macrophages[m])
            #print(direction)
            self.move_agent(self.macrophages[m], direction)
            games = self.check_for_players(self.macrophages[m])
            if len(games) > 0:
                game = random.choice(games)
                if self.macrophages[m].cool_down == 0:
                    #print(str(self.macrophages[m].id)+" spawns a cytokine Z:"+str(self.id_count) + " at " + str(game[1][0]) + ", " + str(game[1][1]))
                    self.spawn_cytokine(game[1])
                    self.macrophages[m].cool_down = 6
            if self.macrophages[m].cool_down > 0:
                self.macrophages[m].cool_down -= 1
        return self.return_state_object().replace("'", '"')

    def return_state_object(self):
        obj = str()
        step = self.step
        self.step += 1
        num_m = len(self.macrophages.keys())
        num_c = len(self.candidae.keys())
        num_z = len(self.cytokines.keys())
        macrophages = list()
        candidae = list()
        cytokines = list()
        for macro in self.macrophages.keys():
            macrophages.append(self.macrophages[macro])
        for candida in self.candidae.keys():
            candidae.append(self.candidae[candida])
        for cyto in self.cytokines.keys():
            cytokines.append(self.cytokines[cyto])
        grid = self.grid.tolist()
        c_grid = self.cytokine_grid.tolist()
        return str(
                {
                    "step": step,
                    "number_of_macrophages": num_m,
                    "number_of_candida": num_c,
                    "number_of_active_cytokines": num_z,
                    "macrophages": macrophages,
                    "candida": candidae,
                    "cytokines": cytokines,
                    "grid": grid,
                    "c_grid": self.cyto_grid_to_json()
                }
            )

    def print_grid(self):
        height, width = np.shape(self.grid)
        for y in range(0,height):
            print(self.grid[y])
    
    def cyto_grid_to_json(self):
        height, width, depth = np.shape(self.cytokine_grid)
        json = {}
        for y in range(0, height):
            for x in range(0, width):
                json[f'{y}:{x}'] = self.cytokine_grid[y,x].tolist()
        return json



        

#print(np.full(np.shape(np.empty(5, dtype=object)), np.array(['',0])))

sim = Simulation(100, 100, 30, 50, 100, 1234)
# sim.print_grid()
for i in range(100):
   sim.run_step()
    #sim.print_grid()
# sim.print_cyto_grid()

