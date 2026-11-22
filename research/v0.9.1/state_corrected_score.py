"""Referee Round 2 correction: AR-working innovation score with observed start.

An exploratory score, NOT a known-correct likelihood for cycles, fractional
integration, or random walks. The starting residual r0 must be computed solely
from the simulated/observed history available at monitoring onset.
"""
import numpy as np
from innovation_detector import unit_drift, RHO

def score(gap, r0, age, rho=RHO, checkpoints=(1, 2, 5, 10)):
    """Whiten residual *levels* r_t=gap_t+r0, not anchored gaps alone.

    z_t = (gap_t-rho*gap_{t-1}) + (1-rho)*r0, with gap_0=0.
    Alternative template a_t=drift_t-rho*drift_{t-1}, drift_0=0.
    Return signed normalized cumulative scores at preset checkpoints.
    """
    gap=np.asarray(gap,dtype=float)
    if gap.ndim!=1 or len(gap)==0 or not np.isfinite(gap).all():
        raise ValueError("gap must be a finite nonempty 1D series")
    if not np.isfinite(r0) or not (0<rho<1):
        raise ValueError("invalid initial residual or rho")
    drift=unit_drift(age,len(gap))
    z=gap-rho*np.r_[0.,gap[:-1]]+(1-rho)*r0
    a=drift-rho*np.r_[0.,drift[:-1]]
    ix=np.minimum((np.array(checkpoints)*365.25).astype(int)-1,len(gap)-1)
    return (np.cumsum(z*a)/np.sqrt(np.cumsum(a*a)))[ix]
