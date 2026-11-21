"""Vintage lower-quantile forecast evaluator (experimental implementation).

Past-only OLS power-law refits at month ends. Two *distinct* illustrative
quantiles are provided: historical Gaussian residual band and conditional
AR(1)-residual predictive band. Neither incorporates parameter uncertainty.
Do NOT treat them as validated P10 forecasts without simulation calibration.
"""
from __future__ import annotations
from dataclasses import dataclass
from statistics import NormalDist
import numpy as np
import pandas as pd

GENESIS = pd.Timestamp('2009-01-03')
Q10 = NormalDist().inv_cdf(.10)

@dataclass(frozen=True)
class VintageSettings:
    burn_in_date: str = '2017-01-31'
    horizons_years: tuple[int, ...] = (1,2,4)
    rho: float = .997
    def __post_init__(self):
        if not 0 < self.rho < 1:
            raise ValueError('rho must be in (0,1)')

def validate(daily: pd.DataFrame) -> pd.DataFrame:
    if not {'date','price_usd'}.issubset(daily.columns):
        raise ValueError('Expected date and price_usd')
    z = daily[['date','price_usd']].copy()
    z['date'] = pd.to_datetime(z.date, utc=True).dt.tz_localize(None).dt.normalize()
    z = z.sort_values('date').reset_index(drop=True)
    if z.date.duplicated().any() or not z.date.diff().dropna().eq(pd.Timedelta(days=1)).all():
        raise ValueError('Require complete, unique UTC daily dates')
    if len(z) < 366 or not np.isfinite(z.price_usd).all() or not (z.price_usd > 0).all():
        raise ValueError('Invalid prices or too few days')
    if (z.date.iloc[0] - GENESIS).days <= 0:
        raise ValueError('Genesis time must be positive')
    return z

def fit_past(prices: np.ndarray, days: np.ndarray) -> tuple[float,float,float,float]:
    x = np.log(days.astype(float)); y = np.log(prices.astype(float))
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (intercept + slope*x)
    return float(intercept),float(slope),float(np.std(resid,ddof=1)),float(resid[-1])

def forecasts(daily: pd.DataFrame, s: VintageSettings=VintageSettings()) -> pd.DataFrame:
    d = validate(daily)
    date_idx = pd.Index(d.date)
    days = (d.date - GENESIS).dt.days.to_numpy()
    prices = d.price_usd.to_numpy(float)
    starts = d.date[d.date.dt.is_month_end & (d.date >= pd.Timestamp(s.burn_in_date))]
    rows=[]
    for vintage in starts:
        end_idx = int(date_idx.get_loc(vintage)) + 1
        if end_idx < 366: continue
        a,b,sd,last_resid = fit_past(prices[:end_idx],days[:end_idx])
        for yr in s.horizons_years:
            target = vintage + pd.DateOffset(years=yr)
            if target not in date_idx: continue
            k = int(date_idx.get_loc(target))
            horizon_days = int((target-vintage).days)
            xfuture = float(np.log(days[k]))
            logtrend = a+b*xfuture
            marginal_p10 = logtrend + Q10*sd
            # Illustrative known-rho Gaussian persistence model; ignores fitting error.
            cf_mean = logtrend + (s.rho**horizon_days)*last_resid
            cf_sd = sd * np.sqrt(1-s.rho**(2*horizon_days))
            conditional_p10 = cf_mean + Q10*cf_sd
            actual_log = float(np.log(prices[k]))
            rows.append({'vintage':vintage.date().isoformat(), 'horizon_years':yr,
                         'target':target.date().isoformat(), 'marginal_breach':bool(actual_log < marginal_p10),
                         'conditional_breach':bool(actual_log < conditional_p10),
                         'marginal_log_deficit':float(actual_log-marginal_p10),
                         'conditional_log_deficit':float(actual_log-conditional_p10),
                         'training_n':end_idx})
    return pd.DataFrame(rows)

def aggregate(rows: pd.DataFrame) -> pd.DataFrame:
    if rows.empty: return pd.DataFrame()
    return rows.groupby('horizon_years',as_index=False).agg(n_vintages=('vintage','size'),
        marginal_breach_fraction=('marginal_breach','mean'),
        conditional_breach_fraction=('conditional_breach','mean'))
