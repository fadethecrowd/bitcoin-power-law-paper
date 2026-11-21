import unittest
import numpy as np
import pandas as pd
from vintage_p10 import VintageSettings, forecasts, aggregate, validate

class VintageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dates=pd.date_range('2010-07-17','2026-08-14',freq='D')
        rng=np.random.default_rng(101)
        days=(dates-pd.Timestamp('2009-01-03')).days.to_numpy()
        prices=np.exp(-37+5.65*np.log(days)+rng.normal(0,.2,len(days)))
        cls.df=pd.DataFrame({'date':dates,'price_usd':prices})
    def test_reject_duplicates(self):
        with self.assertRaises(ValueError): validate(pd.concat([self.df,self.df.tail(1)]))
    def test_reject_missing_dates(self):
        with self.assertRaises(ValueError): validate(self.df.drop(index=100))
    def test_reject_nonpositive(self):
        d=self.df.copy();d.loc[10,'price_usd']=0
        with self.assertRaises(ValueError): validate(d)
    def test_no_lookahead(self):
        cfg=VintageSettings(burn_in_date='2017-01-31',horizons_years=(1,))
        orig=forecasts(self.df,cfg)
        amended=self.df.copy()
        amended.loc[amended.date >= '2020-01-01','price_usd'] *= 20
        changed=forecasts(amended,cfg)
        a=orig[orig.vintage=='2018-01-31'].iloc[0]
        b=changed[changed.vintage=='2018-01-31'].iloc[0]
        self.assertEqual(a.marginal_log_deficit,b.marginal_log_deficit)
        self.assertEqual(a.conditional_log_deficit,b.conditional_log_deficit)
    def test_endpoints_and_training(self):
        rows=forecasts(self.df)
        self.assertFalse(rows.empty)
        self.assertTrue((pd.to_datetime(rows.target)>pd.to_datetime(rows.vintage)).all())
        self.assertTrue((pd.to_datetime(rows.target)<=self.df.date.max()).all())
        self.assertTrue((rows.training_n>=366).all())
        self.assertEqual(set(aggregate(rows).horizon_years), {1,2,4})

if __name__=='__main__': unittest.main()
