"""Declared family of residual (deviation) models and path generators.

Every simulated history is  ln P_t = a + B ln t + u_t  (null: constant B), or
ln P_t = m_D(ln t) + u_t (alternative: declining local exponent), where u_t is
drawn from one member of the declared family below. Processes start at zero
on the genesis day (t = 1) and are observed from t = 560 (2010-07-17), the
same as Baquero & Menezes (Oct 2026); the cycle starts from its stationary
distribution.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
from scipy.signal import lfilter

from . import config as C


@dataclass(frozen=True)
class Model:
    pers: str          # persistence label from config.PERSISTENCE
    kind: str          # "ar" | "rw" | "frac"
    par: float         # rho for AR, d for fractional
    w: float           # cycle variance share
    lam: float         # volatility-shape exponent
    period: float = C.CYCLE_PERIOD_YEARS

    @property
    def id(self) -> str:
        s = f"{self.pers}|cyc{self.w:.1f}|lam{self.lam:g}"
        if self.period != C.CYCLE_PERIOD_YEARS:
            s += f"|P{self.period:g}"
        return s

    def as_dict(self):
        d = asdict(self); d["id"] = self.id; return d


def main_family() -> list[Model]:
    out = []
    for lab, kind, par in C.PERSISTENCE:
        for w in C.CYCLE_WEIGHTS:
            for lam in C.VOL_SHAPES:
                out.append(Model(lab, kind, par, w, lam))
    return out


def volatility_profile(df: pd.DataFrame) -> pd.Series:
    """Annual SD of daily log returns by calendar year (the only real-data input to the
    simulations besides the residual scale). Years before 2010 take the 2010 value."""
    r = np.log(df.price_usd).diff()
    h = r.groupby(df.date.dt.year).std()
    return h


class Generator:
    """Draws deviation paths u (length n, observed days only) for a model."""

    def __init__(self, df: pd.DataFrame, resid_sd: float, x: np.ndarray):
        self.t_obs = df.days_since_genesis.to_numpy()
        self.N = int(self.t_obs[-1])                      # simulate t = 1..N
        self.keep = self.t_obs - 1                        # zero-based positions of observed days
        h = volatility_profile(df)
        years = (pd.Timestamp("2009-01-03") + pd.to_timedelta(np.arange(self.N), unit="D")).year
        hy = np.array([h.get(y, h.iloc[0]) for y in years])
        self.h = hy
        self.resid_sd = resid_sd
        n = len(self.t_obs)
        X1 = np.column_stack([np.ones(n), x - x.mean()])
        self.P1 = np.linalg.pinv(X1)
        self.X1 = X1
        self._frac_cache = {}

    def sigma(self, lam: float) -> np.ndarray:
        s = self.h ** lam
        return s / math.sqrt(np.mean(s[self.keep] ** 2))

    def _detr_sd(self, u: np.ndarray) -> float:
        r = u - self.X1 @ (self.P1 @ u)
        return float(np.std(r, ddof=1))

    def _psi(self, d: float) -> np.ndarray:
        if d not in self._frac_cache:
            k = np.arange(1, self.N)
            psi = np.concatenate([[1.0], np.cumprod((k - 1 + d) / k)])
            self._frac_cache[d] = np.fft.rfft(psi, 2 * self.N)
        return self._frac_cache[d]

    def persistence(self, m: Model, rng: np.random.Generator, sig: np.ndarray) -> np.ndarray:
        e = rng.standard_normal(self.N) * sig
        if m.kind == "ar":
            u = lfilter([1.0], [1.0, -m.par], e)
        elif m.kind == "rw":
            u = np.cumsum(e)
        elif m.kind == "frac":
            u = np.fft.irfft(np.fft.rfft(e, 2 * self.N) * self._psi(m.par), 2 * self.N)[: self.N]
        else:
            raise ValueError(m.kind)
        return u[self.keep]

    def cycle(self, m: Model, rng: np.random.Generator, sig: np.ndarray) -> np.ndarray:
        P = m.period * 365.25
        omega = 2 * math.pi / P
        rho_c = 0.5 ** (1.0 / (C.CYCLE_HALF_LIFE_CYCLES * P))
        coef = rho_c * complex(math.cos(omega), math.sin(omega))
        eta = (rng.standard_normal(self.N) + 1j * rng.standard_normal(self.N)) * sig
        z0 = (rng.standard_normal() + 1j * rng.standard_normal()) * sig[0] / math.sqrt(1 - rho_c ** 2)
        z, _ = lfilter([1.0], [1.0, -coef], eta, zi=[coef * z0])
        return z.real[self.keep]

    def draw(self, m: Model, rng: np.random.Generator) -> np.ndarray:
        sig = self.sigma(m.lam)
        p = self.persistence(m, rng, sig)
        u = p / self._detr_sd(p)
        if m.w > 0:
            c = self.cycle(m, rng, sig)
            u = math.sqrt(1 - m.w) * u + math.sqrt(m.w) * c / self._detr_sd(c)
        return u * (self.resid_sd / self._detr_sd(u))


def trend_deviation(x: np.ndarray, shape: str, delta: float, x_late: float) -> np.ndarray:
    """m_D(x) - B*x for the declining-exponent alternatives (x = ln t).

    linear: beta(x) = B + D*(1/2 - (x-x0)/(x1-x0))  =>  m - Bx = D*[(x-x0)/2 - (x-x0)^2/(2(x1-x0))]
    late:   beta(x) = B for x < xk; B - D*(x-xk)/(x1-xk) after  =>  m - Bx = -D*(x-xk)^2/(2(x1-xk)) for x >= xk
    """
    x0, x1 = x[0], x[-1]
    if shape == "linear":
        z = x - x0
        return delta * (z / 2 - z * z / (2 * (x1 - x0)))
    if shape == "late":
        z = np.clip(x - x_late, 0, None)
        return -delta * z * z / (2 * (x1 - x_late))
    raise ValueError(shape)


def seed_for(stage: str, *keys) -> np.random.SeedSequence:
    """Deterministic, collision-free seeds: (master, stage, model index, ...)."""
    return np.random.SeedSequence([C.MASTER_SEED, C.STAGE[stage], *[int(k) for k in keys]])
