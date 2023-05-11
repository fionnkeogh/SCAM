from agent_based_simulation.agent import Agent, AgentTypes

class Candida(Agent):

    def __init__(self, ID, x = 0, y = 0, d = 0, bounds_x = 30, bounds_y = 30):
        super().__init__(ID, x, y, d, 1, "yellow", AgentTypes.CANDIDA, bounds_x, bounds_y)