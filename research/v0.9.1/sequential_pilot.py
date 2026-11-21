"""Synthetic-only sequential detection feasibility, NOT v0.9 confirmatory inference.

Oracle-like reference: known frozen trend, AR(1) residual with fixed sigma,
no price information and no volatility estimation. Alarm monitors a persistent
negative standardized residual via the lowest (negative) EWMA over the entire
monitoring period. Thresholds are calibrated from disjoint null paths so the
whole-path false-alarm probability, not pointwise size, is controlled.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
import numpy as np

DAYS_PER_YEAR = 365.25
AGE_DAYS = (np.datetime64('2026-08-14') - np.datetime64('2009-01-03')).astype('timedelta64[D]').astype(int)

@dataclass(frozen=True)
class Settings:
    rho: float = .997
    residual_sd: float = .30
    ewma_half_life_days: int = 180
    alpha: float = .05
    years: int = 10
    paths: int = 1500
    seed: int = 20261121
    def __post_init__(self):
        assert 0 < self.rho < 1
        assert self.residual_sd > 0
        assert 0 < self.alpha < 1
        assert self.paths >= 100

def departure(n: int, delta: float, age_days: int = AGE_DAYS) -> np.ndarray:
    """Continuous log-price shortfall when local exponent falls by delta from onset."""
    t = np.arange(1, n + 1, dtype=float)
    return -delta * np.log((age_days + t) / age_days)

def simulate_residuals(s: Settings, seed: int) -> np.ndarray:
    """Returns [days, paths] AR(1) noise, conditioned on residual zero at onset."""
    rng = np.random.default_rng(seed)
    days = int(np.ceil(s.years * DAYS_PER_YEAR))
    sd_innov = s.residual_sd * np.sqrt(1.0 - s.rho ** 2)
    z = np.empty((days, s.paths), dtype=np.float32)
    last = np.zeros(s.paths, dtype=np.float64)
    for d in range(days):
        last = s.rho * last + sd_innov * rng.standard_normal(s.paths)
        z[d] = last
    return z

def alarm_scores(z: np.ndarray, s: Settings, delta: float) -> np.ndarray:
    """EWMA of below-trend log residual; each day smaller means stronger alarm."""
    if z.ndim != 2:
        raise ValueError('paths must be [days, simulations]')
    gamma = 1 - np.exp(-np.log(2) / s.ewma_half_life_days)
    drift = departure(len(z), delta)
    running = np.zeros(z.shape[1])
    scores = np.empty_like(z)
    for day in range(len(z)):
        running = (1 - gamma) * running + gamma * (z[day] + drift[day])
        scores[day] = running
    return scores

def threshold(scores: np.ndarray, alpha: float) -> float:
    minima = scores.min(axis=0)
    return float(np.quantile(minima, alpha, method='lower'))

def first_alarm(scores: np.ndarray, cutoff: float) -> np.ndarray:
    fired = scores <= cutoff
    first = np.argmax(fired, axis=0).astype(float)
    first[~fired.any(axis=0)] = np.nan
    return first + 1

def evaluate(s: Settings, deltas=(0, .5, 1, 3)) -> dict:
    null_cal = alarm_scores(simulate_residuals(s, s.seed + 10), s, 0)
    cutoff = threshold(null_cal, s.alpha)
    del null_cal
    result = {'settings': s.__dict__, 'age_days': int(AGE_DAYS), 'cutoff': cutoff,
              'note': 'AR(1) synthetic-only oracle-trend pilot; NOT the v0.9 screened family'}
    rows = []
    for i, d in enumerate(deltas):
        p = simulate_residuals(s, s.seed + 100 + i)
        alarm = first_alarm(alarm_scores(p, s, d), cutoff)
        horizons = {f'{y}y': round(float(np.mean(alarm <= int(y * DAYS_PER_YEAR))), 4)
                    for y in (1, 2, 5, 10)}
        detected = alarm[np.isfinite(alarm)]
        rows.append({'delta': d, 'detected_by': horizons,
                     'median_detection_years_given_detected':
                         round(float(np.median(detected) / DAYS_PER_YEAR), 3) if len(detected) else None,
                     'n': int(s.paths)})
    result['results'] = rows
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--paths', type=int, default=1500)
    ap.add_argument('--rho', type=float, default=.997)
    args = ap.parse_args()
    print(json.dumps(evaluate(Settings(paths=args.paths, rho=args.rho)), indent=2))

if __name__ == '__main__':
    main()
