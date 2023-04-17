from player import Player
from payoff import Payoff
import random


class Match():

    def __init__(self, player1, player2, payoff, rounds, error):
        self.player_1 = player1
        self.player_2 = player2
        self.score_p1 = 0
        self.score_p2 = 0
        self.payoff = payoff
        self.rounds = rounds
        self.err_rate = error
    
    def play(self):
        for i in range(self.rounds):
            action_p1 = self.player_1.get_action()
            action_p2 = self.player_2.get_action()

            if random.random() <= self.err_rate:
                action_p1 = self.player_1.flip(action_p1)
            if random.random() <= self.err_rate:
                action_p2 = self.player_2.flip(action_p1)

            self.player_1.add_history(action_p1 + action_p2)
            self.player_2.add_history(action_p2 + action_p1)

            result = self.payoff.score(int(action_p1), int(action_p2))
            payoff_p1 = result[0]
            payoff_p2 = result[1]
                                       
            self.score_p1 += payoff_p1
            self.score_p2 += payoff_p2

    def get_results(self):
        return (self.score_p1, self.score_p2)
        
p1 = Player('t4t', '0101')
p2 = Player('coop', '1111')
cc = 3
cd = 0
dc = 5
dd = 1
pay = Payoff(cc, cd, dc, dd)
m = Match(p1, p2, pay, 20, 0.1)
m.play()
print(m.get_results())