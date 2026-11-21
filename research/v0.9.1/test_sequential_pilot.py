import unittest
import numpy as np
from sequential_pilot import Settings, departure, simulate_residuals, alarm_scores, threshold, first_alarm

class PilotTests(unittest.TestCase):
    def test_zero_decline(self):
        self.assertTrue(np.all(departure(40, 0) == 0))
    def test_continuous_anchor(self):
        self.assertEqual(departure(30, 1.0)[0] < 0, True)
        self.assertAlmostEqual(departure(1, 1.0)[0], -np.log1p(1 / 6433), delta=.00001)
    def test_same_seed(self):
        s=Settings(years=1,paths=120)
        self.assertTrue(np.array_equal(simulate_residuals(s,13), simulate_residuals(s,13)))
    def test_no_future_affects_early_scores(self):
        s=Settings(years=1,paths=120)
        x=simulate_residuals(s,13)
        a=alarm_scores(x,s,0)
        x[250:,:] += 1000
        b=alarm_scores(x,s,0)
        self.assertTrue(np.array_equal(a[:250],b[:250]))
    def test_monotone_alternative(self):
        s=Settings(years=1,paths=120)
        x=simulate_residuals(s,13)
        self.assertTrue(np.all(alarm_scores(x,s,1)<=alarm_scores(x,s,0)))
    def test_first_alarm(self):
        x=np.array([[1.,0.],[-2.,-3.],[-4.,2.]])
        self.assertTrue(np.array_equal(first_alarm(x,-2),np.array([2.,2.])))
    def test_null_sample_rate(self):
        s=Settings(years=1,paths=2500)
        c=threshold(alarm_scores(simulate_residuals(s,22),s,0),.05)
        alarm=first_alarm(alarm_scores(simulate_residuals(s,23),s,0),c)
        self.assertLess(abs(np.isfinite(alarm).mean()-.05),.025)

if __name__=='__main__': unittest.main()
