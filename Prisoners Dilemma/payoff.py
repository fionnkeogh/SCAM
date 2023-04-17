class Payoff():

    def __init__(self, cc, cd, dc, dd):
        self.score_comp = [[(dd, dd), (dc, cd)], [(cd, dc), (cc, cc)]]
    
    def score(self, action_p1, action_p2):
        return self.score_comp[action_p1][action_p2]
