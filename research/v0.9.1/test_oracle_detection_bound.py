import unittest
import numpy as np
from statistics import NormalDist
from oracle_detection_bound import AGE,deviation,snr,power

class Tests(unittest.TestCase):
    def test_zero_is_alpha(self):
        self.assertTrue(np.all(deviation(20,0)==0))
        self.assertAlmostEqual(power(0,2),.05,places=12)
    def test_anchor(self):
        self.assertAlmostEqual(deviation(1,1)[0],-np.log1p(1/AGE))
    def test_ramp(self):
        self.assertTrue(np.all(deviation(1000,1,2)>deviation(1000,1)))
    def test_linearity(self):
        self.assertAlmostEqual(snr(2,2),2*snr(1,2))
    def test_horizon(self):
        self.assertLess(power(1,2),power(1,5))
    def test_analytic_vs_normal_mc(self):
        rng=np.random.default_rng(42);n=100000
        s=snr(1,2)
        estimated=np.mean(rng.normal(loc=s,size=n)>NormalDist().inv_cdf(.95))
        self.assertLess(abs(estimated-power(1,2)),.008)

if __name__=="__main__": unittest.main()
