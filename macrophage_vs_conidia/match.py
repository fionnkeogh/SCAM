from macrophage import Macrophage
from candida import Candida
from payoff import Payoff
import random


class Match():

    def __init__(self, macrophage, candida, payoff, rounds, error):
        self.macrophage = macrophage
        self.candida = candida
        self.payoff = payoff
        self.rounds = rounds
        self.err_rate = error
    
    def play(self):
        played_passive = False
        payoff_p1 = 0
        payoff_p2 = 0
        for i in range(self.rounds):
            action_p1 = self.macrophage.get_action()
            action_p2 = self.candida.get_action()

            #print(action_p1)
            #print(action_p2)
            if random.random() <= self.err_rate:
                action_p1 = self.macrophage.flip(action_p1)
            if random.random() <= self.err_rate:
                action_p2 = self.candida.flip(action_p1)

            self.macrophage.add_history(action_p1 + action_p2)
            self.candida.add_history(action_p2 + action_p1)
            result = self.payoff.score(int(action_p1), int(action_p2))
            payoff_p1 += result[0]
            payoff_p2 += result[1]
            
            #if int(action_p1) == 0:
            played_passive = True

        return (payoff_p1, payoff_p2)


    def get_results(self):
        return (self.macrophage.score, self.candida.score)
        
#p1 = Macrophage('passive', '1111')
#p2 = Candida('agressive', '1111')
#pay = Payoff()
#m = Match(p1, p2, pay, 20, 0.1)
#m.play()
#print(m.get_results())