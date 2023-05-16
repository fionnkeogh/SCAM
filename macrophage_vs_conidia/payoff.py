class Payoff():



    def __init__(self, mpp = 1, mpa = 0, map = 2, maa = -2, cpp = 1, cpa = 0, cap = 2, caa = -2):
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
        return self.score_comp[action_p1][action_p2]

