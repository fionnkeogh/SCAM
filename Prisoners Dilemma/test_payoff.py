import unittest
from payoff import Payoff

class TestPayoff(unittest.TestCase):
    
    def test_score(self):
        cc = 3
        cd = 0
        dc = 5
        dd = 1

        test_payoff = Payoff(cc, cd, dc, dd)

        test_cc = test_payoff.score(1, 1)
        self.assertEqual(test_cc[0], cc)
        self.assertEqual(test_cc[1], cc)

        test_cd = test_payoff.score(1, 0)
        self.assertEqual(test_cd[0], cd)
        self.assertEqual(test_cd[1], dc)

        test_dc = test_payoff.score(0, 1)
        self.assertEqual(test_dc[0], dc)
        self.assertEqual(test_dc[1], cd)

        test_dd = test_payoff.score(0, 0)
        self.assertEqual(test_dd[0], dd)
        self.assertEqual(test_dd[1], dd)