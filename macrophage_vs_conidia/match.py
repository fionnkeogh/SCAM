from macrophage_vs_conidia.macrophage import Macrophage
from macrophage_vs_conidia.candida import Candida
from macrophage_vs_conidia.payoff import Payoff
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
            payoff_p1 = result[0]
            payoff_p2 = result[1]
            
            #if int(action_p1) == 0:
            played_passive = True
            
            self.macrophage.add_score(payoff_p1)
            self.candida.add_score(payoff_p2)
        if random.random() <= 0.1:
            mut = random.randint(0, 11)
            if mut <= 5:
                self.macrophage.point_mut()
            elif mut > 5 and mut < 8:
                self.macrophage.decr_memory()
            else:
                self.macrophage.incr_memory()

        if random.random() <= 0.1:
            mut = random.randint(0, 11)
            if mut <= 5:
                self.candida.point_mut()
            elif mut > 5 and mut < 8:
                self.candida.decr_memory()
            else:
                self.candida.incr_memory()
        
        if played_passive:
            return 1
        else:
            return None

    def get_results(self):
        return (self.macrophage.score, self.candida.score)
        
#p1 = Macrophage('passive', '1111')
#p2 = Candida('agressive', '1111')
#pay = Payoff()
#m = Match(p1, p2, pay, 20, 0.1)
#m.play()
#print(m.get_results())