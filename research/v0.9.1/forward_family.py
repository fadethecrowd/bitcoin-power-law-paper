"""Synthetic forward residual-family generator for v0.9.1 (prototype).

No observed future prices. Innovation scales are supplied by pre-onset calibration,
never normalized on future realized trajectories. Component states are warmed up
before onset. NOT the full v0.9 calibrated predictive family yet.
"""
from dataclasses import dataclass
import numpy as np
from scipy.signal import lfilter, fftconvolve

MODELS = (
    'ar0.990|cyc0.8|lam0', 'ar0.990|cyc0.8|lam1',
    'ar0.995|cyc0.4|lam0', 'ar0.995|cyc0.4|lam1',
    'ar0.997|cyc0.4|lam0', 'ar0.997|cyc0.4|lam1',
    'ar0.998|cyc0.4|lam0', 'ar0.998|cyc0.4|lam1',
    'ar0.999|cyc0.4|lam0', 'ar0.999|cyc0.4|lam1',
    'frac0.9|cyc0.8|lam1', 'rw|cyc0.4|lam1',
)

@dataclass(frozen=True)
class Model:
    name: str
    kind: str
    param: float
    cycle_weight: float
    lambda_vol: int

def parse(name: str) -> Model:
    if name not in MODELS:
        raise ValueError('Unscreened model: '+name)
    persistence, cw, lv = name.split('|')
    if persistence.startswith('ar'):
        kind, param = 'ar', float(persistence[2:])
    elif persistence.startswith('frac'):
        kind, param = 'frac', float(persistence[4:])
    elif persistence == 'rw':
        kind, param = 'rw', 1.0
    else:
        raise ValueError(persistence)
    return Model(name,kind,param,float(cw[3:]),int(lv[3:]))

def fractional_weights(d, n):
    w=np.ones(n)
    for k in range(1,n):
        w[k] = w[k-1]*(k-1+d)/k
    return w

def simulate(model_name: str, *, seed: int, forecast_days: int,
             warmup_days: int=7000, persistence_scale: float=.015,
             cycle_scale: float=.015, future_vol_multiplier: float=1.0):
    """Return synthetic onset state and following residuals, not calibrated v0.9 output.

    sigma args are INNOVATION scales provided by pre-onset calibration.
    Future multiplier must be predeclared. No future prices or statistics read.
    Independent RNG streams make horizon-extension reproducible.
    """
    m=parse(model_name)
    if warmup_days < 1000 or forecast_days < 1 or persistence_scale <= 0 or cycle_scale<=0:
        raise ValueError('invalid simulation dimensions/scales')
    if future_vol_multiplier<=0: raise ValueError('vol multiplier')
    rng_p, rng_c = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(2)]
    n=warmup_days+forecast_days
    vol=np.ones(n)
    if m.lambda_vol:
        vol[warmup_days:]=future_vol_multiplier
    e=rng_p.normal(size=n)*vol
    if m.kind=='ar':
        p=lfilter([1],[1,-m.param],e)*persistence_scale
    elif m.kind=='rw':
        p=np.cumsum(e)*persistence_scale
    else:
        w=fractional_weights(m.param,n)
        p=fftconvolve(e,w,mode='full')[:n]*persistence_scale
    period=4*365.25
    decay=0.5**(1/(3*period))
    coeff=decay*np.exp(2j*np.pi/period)
    z=rng_c.normal(size=(n,2))
    ec=(z[:,0]+1j*z[:,1])*vol
    c=lfilter([1],[1,-coeff],ec)*cycle_scale
    residual=np.sqrt(1-m.cycle_weight)*p + np.sqrt(m.cycle_weight)*c.real
    return residual[warmup_days-1:].astype(float)

def anchored_decline(days: int, drop: float, age: int=6432):
    """Log-trend offset relative to fixed-B curve; includes exact day-zero anchor."""
    t=np.arange(days+1,dtype=float)
    return -drop*np.log1p(t/age)
