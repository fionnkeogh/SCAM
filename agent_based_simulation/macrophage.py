import math
from agent_based_simulation.agent import Agent, AgentTypes
from macrophage_vs_conidia.macrophage import Macrophage as MacrophageBrain

class Macrophage(Agent):

    def __init__(self, ID, x = 0, y = 0, d = 0, bounds_x = 30, bounds_y = 30):
        super().__init__(ID, MacrophageBrain(ID, '0101'), x, y, d, 2, "blue", AgentTypes.MACROPHAGE, bounds_x, bounds_y)
    
    def check_for_game(self, pathogens):
        games = list()
        mid = (self.x_pos + self.size*0.5, self.y_pos + self.size*0.5)
        for pathogen in pathogens:
            dist = math.sqrt(abs(pathogen.x_pos-mid[0])**2+abs(pathogen.y_pos-mid[1])**2)
            if dist < 2.0:
                games.append((self, pathogen))
        return games

    def get_max_gradient(self, gradients):
        max_distance = math.inf
        best_gradient = -1
        for i, gradient in enumerate(gradients):
            if gradient[2] < max_distance:
                best_gradient = i
        return best_gradient


    def check_for_gradient(self, cytokines):
        gradients = list()
        for cytokine in cytokines:
            #if cytokine.get_spawner() != self.ID:
            x,y = cytokine.get_position()
            mid = (self.x_pos + self.size*0.5, self.y_pos + self.size*0.5)
            dist = math.sqrt(abs(x-mid[0])**2+abs(y-mid[1])**2)
            gradients.append((self.x_pos-x, self.y_pos-y, dist))
        indx = self.get_max_gradient(gradients)
        if indx >= 0:
            gradient = cytokines[indx]
            print()

    def get_dircetion(self, state):
        cytokines = state.get_cytokine_objects()
        self.check_for_gradient(cytokines)
        return None
    