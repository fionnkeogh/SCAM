import math
from agent_based_simulation.agent import Agent, AgentTypes
from macrophage_vs_conidia.macrophage import Macrophage as MacrophageBrain

class Macrophage(Agent):

    def __init__(self, ID, x = 0, y = 0, d = 0, bounds_x = 30, bounds_y = 30):
        super().__init__(ID, MacrophageBrain(ID, '0101'), x, y, d, 2, "blue", AgentTypes.MACROPHAGE, bounds_x, bounds_y)
    
    def check_for_game(self, pathogens):
        games = list()
        mid = (self.x_pos+0.5, self.y_pos+0.5)
        for pathogen in pathogens:
            dist = math.sqrt(abs(pathogen.x_pos-mid[0])**2+abs(pathogen.y_pos-mid[1])**2)
            if dist < 2.0:
                games.append((self, pathogen))
        return games