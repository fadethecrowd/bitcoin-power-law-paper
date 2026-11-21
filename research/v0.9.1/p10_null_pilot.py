"""Exploratory simple AR(1) reference for historical vintage P10 coverage.
Not the screened 12-model null family. No confidence claim.
"""
from __future__ import annotations
import argparse
import json
import numpy as np
import pandas as pd
from vintage_p10 import forecasts,aggregate,GENESIS

A,B=-37.71919344501603,5.650938373388459
RESID_SD=.6970880734627248
FIRST,LAST='2010-07-17','2026-08-14'

def simulate(seed:int,rho:float) -> pd.DataFrame:
    rng=np.random.default_rng(seed)
    dates=pd.date_range(FIRST,LAST, freq='D')
    days=(dates-GENESIS).days.to_numpy(float)
    noise=np.empty(len(dates),dtype=float)
    noise[0]=rng.normal()*RESID_SD
    innovations=rng.standard_normal(len(dates)-1)*(RESID_SD*np.sqrt(1-rho**2))
    for i in range(1,len(dates)):
        noise[i]=rho*noise[i-1]+innovations[i-1]
    price=np.exp(A+B*np.log(days)+noise)
    return pd.DataFrame({'date':dates,'price_usd':price})

def run(rho:float,n:int=100,seed:int=20261122) -> dict:
    samples={h:[] for h in (1,2,4)}
    for i in range(n):
        agg=aggregate(forecasts(simulate(seed+100*i,rho)))
        for x in agg.itertuples():
            samples[x.horizon_years].append(x.marginal_breach_fraction)
    return {'rho':rho,'n':n,'by_horizon':{str(h):{
        'mean':round(float(np.mean(samples[h])),4),
        'p05':round(float(np.quantile(samples[h],.05)),4),
        'median':round(float(np.median(samples[h])),4),
        'p95':round(float(np.quantile(samples[h],.95)),4),
    } for h in samples},'note':'one simplified stationary AR(1) noise model with published historical SD; exploratory'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=100);args=ap.parse_args()
    for rho in (.995,.997,.999): print(json.dumps(run(rho,args.n),indent=2))
