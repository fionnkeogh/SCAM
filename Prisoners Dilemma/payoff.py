class Payoff():

    def __init__(self, cc, cd, dc, dd):
        self.score_p1 = [[dd, dc], [cd, cc]]
        self.score_p2 = [[dd, cd], [dc, cc]]
    
    def score(self, action_p1, action_p2):
        return [self.score_p1[action_p1][action_p2], self.score_p2[action_p1][action_p2]]
