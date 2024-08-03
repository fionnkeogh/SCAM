class Payoff():



    def __init__(self, *args):
        mpp, mpa, map, maa, cpp, cpa, cap, caa = 0, 0, 0, 0, 0, 0, 0, 0

        if len(args) == 0:
            mpp, mpa, map, maa, cpp, cpa, cap, caa = 1, 0, 2, -2, 1, 0, 2, -2

        elif isinstance(args[0], float):
            mpp, mpa, map, maa, cpp, cpa, cap, caa = args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]
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
        return self.score_comp[action_p1][action_p2]

    def __str__(self):
        return str((self.mpp, self.mpa, self.map, self.maa, self.cpp, self.cpa, self.cap, self.caa))