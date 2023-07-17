from agent import Agent, AgentTypes
import random

class Candida(Agent):
    """
    Candida agent class.
    Inherits all the methods from its parent class 'Agent'.
    """
    
    def __init__(self, ID, x = 0, y = 0, d = 0, bounds_x = 30, bounds_y = 30, strategy = '1010'):
        """
        Candida constructor
        The size is set to 1
        The color is set to yellow
        The agent type is set to AgentTypes.Candida

        Parameters:
        ID (str): The name of the agent
        x (int:): The initial position of the agent on the x-axis
        y (int): The initial position of the agent on the y-axis
        d (int): The initial direction of the agent
        bounds_x (int):
        bounds_y (int):
        strategy (str): The strategy of the agent 
        """
        super().__init__(ID, x, y, d, 1, "yellow", AgentTypes.CANDIDA, bounds_x, bounds_y, strategy)

    def spawn_child(self, x, y):
        """
        This method creates a child from the agent.
        The childs name is the parents name plus the number of the child seperated by a dot.
        The child inherits the parents strategy with a random mutation

        Parameters:
        x (int): The x position where the child should spawn
        y (int): The y position where the child should spawn

        Returns:
        Candida: The child
        """
        self.add_child()
        child_ID = str(self.get_ID()) + '.' + str(self.get_children())
        child = Candida(child_ID, x, y, random.choice([0,1,2,3]), 30, 30, '1010')
        child.random_mut()
        return child
    