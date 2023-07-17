import myLogging as logging
from grid import Grid, Cytokine
from candida import Candida
from macrophage import Macrophage
from match import Match
from payoff import Payoff
import random
import copy
from collections import defaultdict

class State:
    """This class is used to save the state the system is in"""

    def __init__(self, payoff_type):
        """
        Constructor

        Parameters:
        payoff_type (str): The type of payoff that should be used
        """
        self.STATE = {
            'Pathogens': list(),
            'Macrophages': list(),
            'CytokineElements': list(),
            'Grid': list(),
            'PayOff': Payoff(payoff_type),
            "Step": 0,
        }
    
    def add_grid(self, grid):
        """adds a grid to the simulation"""
        if self.get_grid() == None:
            self.STATE["Grid"].append(grid)
            return True
        else:
            return None

    def add_pathogen(self, pathogen):
        """adds a pathogen to the simulation"""
        self.STATE["Pathogens"].append(pathogen)
    
    def add_macrophage(self, macrophage):
        """adds a macrophage to the simulation"""
        self.STATE["Macrophages"].append(macrophage)

    def get_state(self):
        """should return a stringyfied state."""
        step = self.STATE["Step"]
        pathogens = self.STATE["Pathogens"]
        macrophages = self.STATE["Macrophages"]
        cytokineElements = self.STATE["CytokineElements"]
        return [f"At time step: {step}", *pathogens, *macrophages, *cytokineElements]
    
    def get_grid(self):
        """returns the grid as a string"""
        if len(self.STATE["Grid"]) > 0:
            return str(self.STATE["Grid"][0])
        else:
            return None
        
    def get_size_of_state(self):
        """Returns a string with the size of the states properties"""
        return {
            "Pathogens": len(self.STATE["Pathogens"]),
            "Macrophages": len(self.STATE["Macrophages"]),
            "CytokineElements": len(self.STATE["CytokineElements"]),
            "Grid": self.STATE["Grid"][0].get_size()
        }
    
    def init_possible_positions(self):
        """returns empty positions on the grid"""
        if self.get_grid() == None:
            return None
        else:
            return self.STATE["Grid"][0].get_init_positions()
        
    def init_possible_border_positions(self):
        """returns empty positions at the borders of the grid"""
        pass

    def get_agents(self):
        """returns all agents"""
        return [*self.STATE["Pathogens"], *self.STATE["Macrophages"]]
    
    def get_macrophage_objects(self):
        """retruns macrophage agents"""
        return [*self.STATE["Macrophages"]]
    
    def get_pathogen_objects(self):
        """returns candida agents"""
        return [*self.STATE["Pathogens"]]

    def get_payoff(self):
        """returns the payoff matrix"""
        return self.STATE["PayOff"]
    
    def get_time(self):
        """returns the time step"""
        return self.STATE["Step"]

    def increase_time(self):
        """increases the time by 1"""
        self.STATE["Step"] += 1

    
class Simulation:
    """This class handles the actual simulation"""
    def __init__(self, args):
        """
        Constructor

        Parameters:
        size (tuple): dimensions of the grid
        num_path (int): number of pathogens
        num_phages (int): number of macrophages        
        """
        self.logger = logging.Logger()
        if(len(args) < 1):
            self.size = (100, 100)
            self.num_path = 70
            self.num_phages = 30
        else:
            self.size = (args[0], args[1])
            self.num_path = args[2]
            self.num_phages = args[3]
            self.payoff = args[4] if len(args) >= 5 else None
        
        self.logger.log("Size of world: "+str(self.size))
        self.logger.log("Number of Pathogens: " + str(self.num_path))
        self.logger.log("Number of Macrophages: " + str(self.num_phages))
        self.STATE = State(str(self.payoff))
        print(self.STATE.get_payoff())
        if self.STATE.add_grid(Grid(self.size)) == None:
            self.logger.error("Grid could not be initilized!")
        possible_positions = self.STATE.init_possible_positions()
        if possible_positions == None:
            self.logger.error("No grid to get positions for.")
        self.init_pathogens(self.num_path, possible_positions, self.size)
        self.init_macrophages(self.num_phages, possible_positions, self.size)
        self.logger.log_state(self.STATE.get_state())

    def get_random_strategy_of_length(self, length):
        """returns a random strategy of a given length"""
        strat = ''
        for i in range(length):
            strat.append(random.choice['0', '1'])
        return strat

    def init_pathogens(self, number_of_pathogens, possible_positions, size):
        """
        Creates the pathogens for the simulation

        Parameters:
        number_of_pathogens (int): The number of pathogens to be simulated
        possible_positions (list): A list with possible starting positions for the pathogens
        size (tuple): thse size of the grid
        """
        for p in range(number_of_pathogens):
            l = self.STATE.get_size_of_state()["Pathogens"]
            id = f"P{l}"
            pos = random.choice(list(possible_positions.keys()))
            possible_positions.pop(pos)
            pos = str(pos).replace("(", "").replace(")", "").split(",")
            y = int(pos[0])*2+random.randint(0, 1)
            x = int(pos[1])*2+random.randint(0, 1)
            pathogen = Candida(id, x, y, bounds_x=size[1], bounds_y=size[0], strategy=self.get_random_strategy_of_length(4))
            self.STATE.add_pathogen(pathogen)
    
    def init_macrophages(self, number_of_macrophages, possible_positions, size):
        """
        Creates the macrophages for the simulation

        Parameters:
        number_of_macrophages (int): The number of pathogens to be simulated
        possible_positions (list): A list with possible starting positions for the macrophages
        size (tuple): thse size of the grid
        """
        for m in range(number_of_macrophages):
            l = self.STATE.get_size_of_state()["Macrophages"]
            id = f"M{l}"
            pos = random.choice(list(possible_positions.keys()))
            possible_positions.pop(pos)
            pos = str(pos).replace("(", "").replace(")", "").split(",")
            y = int(pos[0])*2
            x = int(pos[1])*2
            macrophage = Macrophage(id, x, y, bounds_x=size[1], bounds_y=size[0], strategy=self.get_random_strategy_of_length(4))
            self.STATE.add_macrophage(macrophage)

    # TODO
    def step(self):
        pass
    
    def selection(self, rank):
        """
        This method is responsible for the selection process.
        It choses the macrophages with the best scores and produces children for them.
        The macrophages with the worst scores are killed off.

        Parameters:
        rank (int): The number how many parents are chosen and how many are killed
        """
        macrophages = self.STATE.get_macrophage_objects()
        scores = {}
        for macrophage in macrophages:
            score = macrophage.get_score()
            name = macrophage.get_ID()
            scores[macrophage] = score
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1]))
        parents = list(dict(sorted_scores).keys())[-rank:]
        middle = list(dict(sorted_scores).keys())[-rank:rank]
        losers = list(dict(sorted_scores).keys())[:rank]
        children = list()
        possible_positions = self.STATE.init_possible_positions()
        if possible_positions == None:
            self.logger.error("No grid to get positions for.")
        for parent in parents:
            pos = random.choice(list(possible_positions.keys()))
            possible_positions.pop(pos)
            pos = str(pos).replace("(", "").replace(")", "").split(",")
            y = int(pos[0])*2
            x = int(pos[1])*2
            children.append(parent.spawn_child(x, y))
        updated_macros = parents + middle + children
        for loser in losers:
            self.STATE["Macrophages"]
        for macro in updated_macros:
            self.STATE.add_macrophage(macro)