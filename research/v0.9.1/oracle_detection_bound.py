"""Idealized fixed-horizon Gaussian AR(1) change-detection calculation.

Synthetic/analytic benchmark, not a trained Bitcoin detector. Known onset,
known abrupt or two-year ramp decline, stationary AR(1) noise with known
residual SD and rho; observation at exact fixed horizon. Null and alternative
share residual starting value zero. Simple-vs-simple Neyman-Pearson power at
one-sided alpha, with no sequential multiple-testing adjustment.
"""
from __future__ import annotations
from math import erf, sqrt
from statistics import NormalDist
import numpy as np

GENESIS = np.datetime64("2009-01-03")
ONSET = np.datetime64("2026-08-14")
AGE = int((ONSET-GENESIS)/np.timedelta64(1,"D"))

def deviation(n: int, drop: float, ramp_years: float = 0) -> np.ndarray:
    """Continuous log-price difference for a decline in local log/log slope."""
    t = np.arange(1,n+1,dtype=float)
    if ramp_years == 0:
        return -drop*np.log1p(t/AGE)
    r = 365.25*ramp_years
    z = np.minimum(t,r)
    early = -drop*(z-AGE*np.log1p(z/AGE))/r
    tail = np.where(t>r, -drop*np.log((AGE+t)/(AGE+r)), 0)
    return early+tail

def snr(drop: float, years: float, rho: float=.997, residual_sd:float=.30,
        ramp_years:float=0) -> float:
    assert 0<rho<1 and residual_sd>0
    m=deviation(round(years*365.25),drop,ramp_years)
    innovation_mean=m-rho*np.r_[0,m[:-1]]
    innovation_sd=residual_sd*np.sqrt(1-rho**2)
    return float(np.linalg.norm(innovation_mean)/innovation_sd)

def power(drop:float,years:float,rho:float=.997,residual_sd:float=.30,
          alpha:float=.05,ramp_years:float=0) -> float:
    z=snr(drop,years,rho,residual_sd,ramp_years)-NormalDist().inv_cdf(1-alpha)
    return float((1+erf(z/sqrt(2)))/2)

if __name__=="__main__":
    for shape,ramp in [("step",0),("2-year ramp",2)]:
        for rho in (.995,.997,.999):
            for d in (0,.5,1,3):
                print(shape,rho,d,*(round(power(d,y,rho,ramp_years=ramp),4) for y in (1,2,5,10)))
