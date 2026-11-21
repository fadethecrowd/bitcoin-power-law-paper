import unittest
import numpy as np
from forward_family import MODELS, parse, simulate, anchored_decline

class Tests(unittest.TestCase):
    def test_all_twelve(self):
        self.assertEqual(len(MODELS),12)
        for model in MODELS: self.assertEqual(parse(model).name,model)
    def test_no_unsupported(self):
        with self.assertRaises(ValueError): parse('ar0.1|cyc0.4|lam1')
    def test_reproducible(self):
        for name in MODELS:
            a=simulate(name,seed=12,forecast_days=30,warmup_days=1000)
            b=simulate(name,seed=12,forecast_days=30,warmup_days=1000)
            self.assertTrue(np.array_equal(a,b))
    def test_no_future_volatility_for_lam0(self):
        a=simulate(MODELS[0],seed=33,forecast_days=90,warmup_days=1000,future_vol_multiplier=1)
        b=simulate(MODELS[0],seed=33,forecast_days=90,warmup_days=1000,future_vol_multiplier=3)
        self.assertTrue(np.array_equal(a,b))
    def test_anchored(self):
        self.assertEqual(anchored_decline(100,1)[0],0)
        self.assertTrue(np.all(np.diff(anchored_decline(100,1))<0))
    def test_no_future_horizon_leakage(self):
        for name in MODELS:
            short=simulate(name,seed=42,forecast_days=60,warmup_days=1000)
            long=simulate(name,seed=42,forecast_days=90,warmup_days=1000)
            self.assertTrue(np.allclose(short,long[:61],rtol=0,atol=1e-10),name)
    def test_shape(self):
        for model in MODELS:
            x=simulate(model,seed=5,forecast_days=60,warmup_days=1000)
            self.assertEqual(len(x),61)
            self.assertTrue(np.isfinite(x).all())

if __name__=='__main__': unittest.main()
