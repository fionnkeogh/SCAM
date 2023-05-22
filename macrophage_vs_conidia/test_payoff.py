import unittest
from macrophage_vs_conidia.payoff import Payoff

class TestPayoff(unittest.TestCase):
    
    def test_score(self):
        mpp = 1
        mpa = 0
        map = 2
        maa = -2
        cpp = 1
        cpa = 0
        cap = 2
        caa = -2

        test_payoff = Payoff()

        test_pp = test_payoff.score(0, 0)
        self.assertEqual(test_pp[0], mpp)
        self.assertEqual(test_pp[1], cpp)

        test_pa = test_payoff.score(0, 1)
        self.assertEqual(test_pa[0], mpa)
        self.assertEqual(test_pa[1], cap)

        test_ap = test_payoff.score(1, 0)
        self.assertEqual(test_ap[0], map)
        self.assertEqual(test_ap[1], cpa)

        test_aa = test_payoff.score(1, 1)
        self.assertEqual(test_aa[0], maa)
        self.assertEqual(test_aa[1], caa)