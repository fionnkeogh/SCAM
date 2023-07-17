class Payoff():
    """Payoff matrix to determine the score of both players"""

    def __init__(self, *args):
        """
        Constructor
        If no parameters are given it uses a hawk dove payoff matrix.
        You can give the 8 values directly as parameters.
        Alternatively it possible to chose from 3 premade payoff matrices.
        Choices are: "patho1", "patho2" or "alien"
        """

        if len(args) == 0:
            mpp, mpa, map, maa, cpp, cpa, cap, caa = 1, 0, 2, -2, 1, 0, 2, -2

        elif isinstance(args[0], int):
            mpp, mpa, map, maa, cpp, cpa, cap, caa = args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]
        
        elif isinstance(args[0], str):
            if args[0] == 'patho1':
                mpp, mpa, map, maa, cpp, cpa, cap, caa = 5, 0, 3, 1, 5, 0, 6, 1
            
            elif args[0] == 'patho2':
                mpp, mpa, map, maa, cpp, cpa, cap, caa = 5, 0, 3, 1, 5, 0, 4, 1

            elif args[0] == 'alien':
                mpp, mpa, map, maa, cpp, cpa, cap, caa = 3, 1, 0, 2, 2, 0, 1, 1

        self.mpp = mpp
        self.mpa = mpa
        self.map = map
        self.maa = maa
        self.cpp = cpp
        self.cpa = cpa
        self.cap = cap
        self.caa = caa

        self.score_comp = [[(self.mpp, self.cpp), (self.mpa, self.cap)], [(self.map, self.cpa), (self.maa, self.caa)]]
        self.score_macro = [[self.mpp, self.mpa], [self.map, self.maa]]
        self.score_candida = [[self.cpp, self.cap], [self.cpa, self.caa]]
    
    def score(self, action_p1, action_p2):
        """
        This method determines the score for both players given their 2 actions
        
        Paramezers:
        action_p1 (int): The action of player 1
        action_p2 (int): The action of player 2

        Returns:
        tuple (score player 1, score player 2)
        """
        return self.score_comp[action_p1][action_p2]

    def __str__(self):
        """To string method"""
        return str((self.mpp, self.mpa, self.map, self.maa, self.cpp, self.cpa, self.cap, self.caa))