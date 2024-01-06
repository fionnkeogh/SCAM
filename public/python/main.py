import random
from python.simulation import Simulation, Macrophage, Candida, Cytokine, Player
# from python.grid import Grid
# from python.cytokine import Cytokine
# from python.macrophage import Macrophage
# from python.candida import Candida


# class Simulation:
#     """This class handles the actual simulation"""
#     def __init__(self, args: list):
#         """
#         Constructor

#         Parameters:
#         size (tuple): dimensions of the grid
#         num_path (int): number of pathogens
#         num_phages (int): number of macrophages        
#         """
#         self.grid: Grid = None
#         if(len(args) < 1):
#             self.grid = Grid(100, 100)
#             num_path = 70
#             num_phages = 30
#             self.simulation_length = 100
#         else:
#             print(args)
#             self.grid = Grid(args[0][0], args[0][1])
#             num_path = args[1]
#             num_phages = args[2]
#             self.simulation_length = args[3]
            
#         self.steps = 0
#         self.grid.update_spawns(2)
#         self.ids = 1000000
#         self.macrophages: list[Macrophage] = []
#         self.candida: list = []
#         self.cytokines: list[Cytokine] = [Cytokine(self.ids, 5, 5, radius=5)] #Cytokine(5, 5, radius=5)
#         for i in range(num_phages):
#             x, y = self.grid.get_spawn_position(2)
#             self.macrophages.append(Macrophage(self.ids, x,y, self.grid))
#             self.ids += 1

#         self.grid.update_spawns()
#         for i in range(num_path):
#             x, y = self.grid.get_spawn_position(1)
#             self.candida.append(Candida(self.ids, x,y, self.grid))
#             self.ids += 1

    
#     def start_new_simulation(self) -> None:
#         print("Starting new Simulation.")
    
#     def get_grid(self) -> str:
#         print("Getting Grid")
#         return str({"x":self.grid.get_size()[1],"y":self.grid.get_size()[0]})
    
#     def get_macrophages(self) -> str:
#         return str(self.macrophages)

#     def get_candida(self) -> str:
#         return str(self.candida)

#     def get_cytokines(self) -> str:
#         return str(self.cytokines)
    
#     def update(self) -> None:
#         if self.steps < self.simulation_length:
#             self.update_cytokines()
#             self.update_macrophages()
#             self.steps += 1
    
#     def update_cytokines(self) -> None:
#         for i in range(len(self.cytokines)):
#             cytokine = self.cytokines[i]
#             firing = cytokine.update()
#             if firing == False:
#                 self.cytokines.pop(i)

#     def update_macrophages(self) -> None:
#         for i in range(len(self.macrophages)):
#             macrophage = self.macrophages[i]
#             macrophage.update(self.grid)

def init_simulation(width: int = 10, height: int = 10, num_m: int = 3, num_c: int = 5, max_steps: int = 100, seed: int = 1234) -> Simulation:
    global simulation
    simulation = Simulation(width, height, num_m, num_c, max_steps, seed)
    return simulation

def get_simulation() -> Simulation:
    return simulation
