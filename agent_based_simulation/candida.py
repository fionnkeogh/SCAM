from agent_based_simulation.agent import Agent, AgentTypes
from macrophage_vs_conidia.candida import Candida as CandidaBrain

class Candida(Agent):

    def __init__(self, ID, x = 0, y = 0, d = 0, bounds_x = 30, bounds_y = 30):
        super().__init__(ID, CandidaBrain(ID, '0101'), x, y, d, 1, "yellow", AgentTypes.CANDIDA, bounds_x, bounds_y)

    def move(self, direction = None, step = 1):
        pass