import agent_based_simulation.myLogging as logging
from agent_based_simulation.grid import Grid, Cytokine
from agent_based_simulation.candida import Candida
from agent_based_simulation.macrophage import Macrophage
from macrophage_vs_conidia.match import Match
from macrophage_vs_conidia.payoff import Payoff
import random
import copy

class State:
    def __init__(self, payoff_type):
        self.STATE = {
            'Pathogens': list(),
            'Macrophages': list(),
            'CytokineElements': list(),
            'Grid': list(),
            'PayOff': Payoff(payoff_type),
            "Step": 0,
            'MacrophageStrategies': dict(),
            'PathogenStrategies': dict()
        }
    
    def add_grid(self, grid):
        if self.get_grid() == None:
            self.STATE["Grid"].append(grid)
            return True
        else:
            return None

    def add_pathogen(self, pathogen):
        self.STATE["Pathogens"].append(pathogen)
    
    def add_macrophage(self, macrophage):
        self.STATE["Macrophages"].append(macrophage)

    def add_cytokine(self, macrophage):
        pos = (macrophage.x_pos, macrophage.y_pos)
        for cytokine in self.STATE["CytokineElements"]:
            if cytokine.get_position() == (pos[0]+1,pos[1]+1):
                return None
            if cytokine.get_position() == (pos[0]+0,pos[1]+1):
                return None
            if cytokine.get_position() == (pos[0]+1,pos[1]+0):
                return None
            if cytokine.get_position() == (pos[0]+0,pos[1]+0):
                return None
            if cytokine.get_position() == (pos[0]-1,pos[1]-1):
                return None
            if cytokine.get_position() == (pos[0]-0,pos[1]-1):
                return None
            if cytokine.get_position() == (pos[0]-1,pos[1]-0):
                return None
            if cytokine.get_position() == (pos[0]-0,pos[1]-0):
                return None
        self.STATE["CytokineElements"].append(Cytokine(len(self.STATE["CytokineElements"]), 2, pos, (115, 9, 9), macrophage.ID))

    def remove_cytokine(self, cytokine):
        self.STATE["CytokineElements"].remove(cytokine)

    def get_state(self):
        # should return a stringyfied state.
        step = self.STATE["Step"]
        pathogens = self.STATE["Pathogens"]
        macrophages = self.STATE["Macrophages"]
        cytokineElements = self.STATE["CytokineElements"]
        return [f"At time step: {step}", *pathogens, *macrophages, *cytokineElements]

    def get_grid(self):
        if len(self.STATE["Grid"]) > 0:
            return str(self.STATE["Grid"][0])
        else:
            return None

    def get_size_of_state(self):
        return {
            "Pathogens": len(self.STATE["Pathogens"]),
            "Macrophages": len(self.STATE["Macrophages"]),
            "CytokineElements": len(self.STATE["CytokineElements"]),
            "Grid": self.STATE["Grid"][0].get_size()
        }

    def init_possible_positions(self):
        if self.get_grid() == None:
            return None
        else:
            return self.STATE["Grid"][0].get_init_positions()

    def get_agents(self):
        return [*self.STATE["Pathogens"], *self.STATE["Macrophages"]]
    
    def get_macrophage_objects(self):
        return [*self.STATE["Macrophages"]]
    
    def get_pathogen_objects(self):
        return [*self.STATE["Pathogens"]]

    def get_cytokine_objects(self):
        return [*self.STATE["CytokineElements"]]

    def get_payoff(self):
        return self.STATE["PayOff"]

    def increase_time(self):
        self.STATE["Step"] += 1

    def get_macrophage_strategies(self):
        return self.STATE["MacrophageStrategies"]
    
    def get_pathogen_strategies(self):
        return self.STATE["PathogenStrategies"]
    
    def update_strategies(self):
        macrophage_strats = {}
        for macrophage in self.get_macrophage_objects():
            strat = macrophage.brain.get_strategy()
            if strat in macrophage_strats:
                macrophage_strats.update({strat: macrophage_strats.get(strat) + 1})
            else:
                macrophage_strats.update({strat: 1})
        self.STATE.update({'MacrophageStrategies': macrophage_strats})
        
        pathogen_strats = {}
        for pathogen in self.get_pathogen_objects():
            strat = pathogen.brain.get_strategy()
            if strat in pathogen_strats:
                pathogen_strats.update({strat: pathogen_strats.get(strat) + 1})
            else:
                pathogen_strats.update({strat: 1})
        self.STATE.update({'PathogenStrategies': pathogen_strats})
        
    

class Simulation:
    def __init__(self, args):
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


    def init_pathogens(self, number_of_pathogens, possible_positions, size):
        for p in range(number_of_pathogens):
            l = self.STATE.get_size_of_state()["Pathogens"]
            id = f"P{l}"
            pos = random.choice(list(possible_positions.keys()))
            possible_positions.pop(pos)
            pos = str(pos).replace("(", "").replace(")", "").split(",")
            y = int(pos[0])*2+random.randint(0, 1)
            x = int(pos[1])*2+random.randint(0, 1)
            pathogen = Candida(id, x, y, bounds_x=size[1], bounds_y=size[0])
            self.STATE.add_pathogen(pathogen)
    
    def init_macrophages(self, number_of_macrophages, possible_positions, size):
        for m in range(number_of_macrophages):
            l = self.STATE.get_size_of_state()["Macrophages"]
            id = f"M{l}"
            pos = random.choice(list(possible_positions.keys()))
            possible_positions.pop(pos)
            pos = str(pos).replace("(", "").replace(")", "").split(",")
            y = int(pos[0])*2
            x = int(pos[1])*2
            macrophage = Macrophage(id, x, y, bounds_x=size[1], bounds_y=size[0])
            self.STATE.add_macrophage(macrophage)
    
    def step(self):
        self.logger.log("NEXT STEP:")
        self.STATE.increase_time()
        for obj in self.STATE.get_agents():
            if(type(obj) == Macrophage):
                obj.get_dircetion(copy.deepcopy(self.STATE))
            obj.update()
        for obj in self.STATE.get_cytokine_objects():
            delete = obj.update()
            if delete != None:
                self.STATE.remove_cytokine(obj)
        games = list()
        pathogens = self.STATE.get_pathogen_objects()
        for macrophage in self.STATE.get_macrophage_objects():
            games.extend(macrophage.check_for_game(pathogens))
        self.play_games(games)
        self.STATE.update_strategies()
        self.logger.log_state(self.STATE.get_state())

    def play_games(self, games):
        self.logger.log("GAMES:")
        for game in games:
            match = Match(game[0].brain, game[1].brain, self.STATE.get_payoff(), 5, 0.1)
            played_passive = match.play()
            if played_passive != None:
                self.STATE.add_cytokine(game[0])
            self.logger.log(str(match.get_results()))