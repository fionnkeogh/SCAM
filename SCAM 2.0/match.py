from macrophage_vs_conidia.macrophage import Macrophage
from macrophage_vs_conidia.candida import Candida
from macrophage_vs_conidia.payoff import Payoff
import random


class Match():
    """This class matches up a macrophage and a candida to let them play against each other"""

    def __init__(self, macrophage, candida, payoff, rounds, error):
        """"
        Constructor

        Parameters:
        macrophage (Macrophage): The macrophage agent
        candida (Candida): The candida agent
        payoff (Payoff): The payoff matrix to be used
        round (int): The number of rounds the players should play against erach other
        error (float): the error rate of both players when chosing an action
        """
        self.macrophage = macrophage
        self.candida = candida
        self.payoff = payoff
        self.rounds = rounds
        self.err_rate = error
        self.candida_score = 0
        self.macrophage_score = 0
    
    def play(self, mut_rate=0.0):
        """
        This method lets the two agents play against each other.
        Afterwards both mutate with a certain probability

        Parameters:
        mut (float): The probability with which the agents will mutate after playing
        """
        for i in range(self.rounds):
            action_p1 = self.macrophage.get_action()
            action_p2 = self.candida.get_action()


            if random.random() <= self.err_rate:
                action_p1 = self.macrophage.flip(action_p1)
            if random.random() <= self.err_rate:
                action_p2 = self.candida.flip(action_p1)

            self.macrophage.add_history(action_p1 + action_p2)
            self.candida.add_history(action_p2 + action_p1)

            result = self.payoff.score(int(action_p1), int(action_p2))
            payoff_p1 = result[0]
            payoff_p2 = result[1]
            
            self.macrophage.add_score(payoff_p1)
            self.candida.add_score(payoff_p2)
            self.macrophage_score += payoff_p1
            self.candida_score += payoff_p2

        if random.random() <= mut_rate:
            mut = random.randint(0, 11)
            if mut <= 5:
                self.macrophage.point_mut()
            elif mut > 5 and mut < 8:
                self.macrophage.decr_memory()
            else:
                self.macrophage.incr_memory()

        if random.random() <= mut_rate:
            mut = random.randint(0, 11)
            if mut <= 5:
                self.candida.point_mut()
            elif mut > 5 and mut < 8:
                self.candida.decr_memory()
            else:
                self.candida.incr_memory()


    def get_results(self):
        """returns the scores of both players from this match only"""
        return (self.macrophage_score, self.candida_score)
        
#p1 = Macrophage('passive', '1111')
#p2 = Candida('agressive', '1111')
#pay = Payoff()
#m = Match(p1, p2, pay, 20, 0.1)
#m.play()
#print(m.get_results())