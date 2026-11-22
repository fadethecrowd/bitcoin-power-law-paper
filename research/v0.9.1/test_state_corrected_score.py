import unittest
import numpy as np
from state_corrected_score import score
from innovation_detector import score_innovations

class TestStateCorrected(unittest.TestCase):
    def test_level_formula(self):
        rho=.997;age=6432;rng=np.random.default_rng(10)
        r=np.r_[.8,.8+rng.normal(size=3653).cumsum()*.015]
        gap=r[1:]-r[0]
        d=-np.log1p(np.arange(1,len(gap)+1)/age)
        a=d-rho*np.r_[0,d[:-1]]
        z=r[1:]-rho*r[:-1]
        ix=np.array([int(y*365.25)-1 for y in (1,2,5,10)])
        expected=(np.cumsum(z*a)/np.sqrt(np.cumsum(a*a)))[ix]
        np.testing.assert_allclose(score(gap,r[0],age),expected,rtol=1e-12,atol=1e-12)
    def test_zero_start_matches_original(self):
        x=np.zeros(3653)
        np.testing.assert_allclose(score(x,0,6432),score_innovations(x,6432))
    def test_nonzero_level_changes_score(self):
        self.assertTrue(np.any(score(np.zeros(3653),.8,6432)!=0))
    def test_no_future_leakage(self):
        g=np.arange(3653)/3653
        original=score(g,.4,6432)
        g[800:]=1e9
        changed=score(g,.4,6432)
        np.testing.assert_array_equal(original[:2],changed[:2])
    def test_start_sign_effect(self):
        x=np.zeros(3653)
        self.assertFalse(np.array_equal(score(x,.7,6432),score(x,-.7,6432)))

if __name__=='__main__':unittest.main()
