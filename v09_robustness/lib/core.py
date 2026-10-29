"""Data loading, design indices and fast estimators.

All regressions are ln P on ln t (t = days since 2009-01-03), unweighted OLS
with a free intercept, matching the v0.8 conventions. Fast estimators use
cumulative sums so the same code runs on the real series and on hundreds of
thousands of simulated paths.

Nothing in this module writes data to disk.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from . import config as C


# ------------------------------------------------------------------ data ---
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_data(path: Path, require_frozen: bool = True) -> pd.DataFrame:
    df = pd.read_csv(path)
    need = {"date", "timestamp", "price_usd", "days_since_genesis"}
    if need - set(df.columns):
        raise ValueError(f"missing columns: {sorted(need - set(df.columns))}")
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df = df.sort_values("date").reset_index(drop=True)
    if (df.price_usd <= 0).any() or df.date.duplicated().any():
        raise ValueError("non-positive prices or duplicate dates")
    if (df.date.diff().iloc[1:] != pd.Timedelta(days=1)).any():
        raise ValueError("date gaps")
    if not np.array_equal((df.date - C.GENESIS).dt.days.to_numpy(), df.days_since_genesis.to_numpy()):
        raise ValueError("days_since_genesis must equal (date - 2009-01-03).days")
    if require_frozen and (len(df) != C.FROZEN_N or df.date.iloc[0] != C.FROZEN_FIRST
                           or df.date.iloc[-1] != C.FROZEN_LAST):
        raise ValueError("not the frozen v0.8 sample shape; pass --allow-different-sample")
    return df


# ---------------------------------------------------------------- design ---
@dataclass
class Design:
    """Everything about the sample that does not depend on prices."""
    dates: pd.DatetimeIndex
    t: np.ndarray            # days since genesis
    x: np.ndarray            # ln t
    n: int
    xc: np.ndarray = field(init=False)
    Sx: np.ndarray = field(init=False)
    Sxx: np.ndarray = field(init=False)

    def __post_init__(self):
        self.xm = float(self.x.mean())
        self.xc = self.x - self.xm                        # centring improves cumsum precision
        self.Sx = np.concatenate([[0.0], np.cumsum(self.xc)])
        self.Sxx = np.concatenate([[0.0], np.cumsum(self.xc * self.xc)])
        d = self.dates
        self.idx = {dt: i for i, dt in enumerate(d)}
        # month-end evaluation points: last available day of each calendar month
        me = pd.Series(np.arange(self.n), index=d).groupby([d.year, d.month]).max().to_numpy()
        self.month_end = me
        self.i_post = int(np.searchsorted(d.values, np.datetime64(C.POST_START)))
        # rolling-window start index for every end index and window length
        self.roll_start = {}
        for L in C.ROLL_YEARS:
            starts = np.searchsorted(d.values, (d - pd.DateOffset(years=L)).values, side="right")
            self.roll_start[L] = starts
        # rolling evaluation points: month-ends whose window is complete, plus the final day
        self.roll_eval = {}
        for L in C.ROLL_YEARS:
            first_full = d[0] + pd.DateOffset(years=L)
            ev = me[d[me] >= first_full]
            if ev[-1] != self.n - 1:
                ev = np.append(ev, self.n - 1)
            self.roll_eval[L] = ev
        self.named = np.array([self.idx[pd.Timestamp(s)] for s in C.NAMED_ENDS])
        self.year_start_idx = np.array([self.idx[pd.Timestamp(s)] for s in C.YEAR_STARTS])
        # expanding evaluation points: month-ends from January 2017
        self.exp_eval = me[me >= self.i_post]
        # quadratic-in-ln-t weights for the curvature coefficient (exact OLS)
        X = np.column_stack([np.ones(self.n), self.xc, self.xc ** 2])
        self.w_quad = np.linalg.pinv(X)[2]
        X1 = np.column_stack([np.ones(self.n), self.xc])
        self.P1 = np.linalg.pinv(X1)                      # 2 x n
        self.x_span = float(self.x[-1] - self.x[0])
        # monthly series for the break detector (last close of each calendar month)
        self.monthly = me
        # halving epochs: E0 partial start, E1..E3 complete, E4 incomplete
        cuts = [0] + [self.idx[pd.Timestamp(h)] for h in C.HALVINGS] + [self.n]
        self.epochs = [(cuts[k], cuts[k + 1]) for k in range(len(cuts) - 1)]


def design_from_df(df: pd.DataFrame) -> Design:
    t = df.days_since_genesis.to_numpy(float)
    return Design(dates=pd.DatetimeIndex(df.date), t=t, x=np.log(t), n=len(df))


# ------------------------------------------------------------ estimators ---
def ols(xc: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    xm = xc.mean(); ym = y.mean(); dx = xc - xm
    b = float(np.dot(dx, y - ym) / np.dot(dx, dx))
    return b, float(ym - b * xm)


def slopes_window(D: Design, Sy: np.ndarray, Sxy: np.ndarray, i0: np.ndarray, i1: np.ndarray) -> np.ndarray:
    """OLS slopes over inclusive index windows [i0, i1] using cumulative sums."""
    m = i1 - i0 + 1
    sx = D.Sx[i1 + 1] - D.Sx[i0]; sy = Sy[i1 + 1] - Sy[i0]
    sxx = D.Sxx[i1 + 1] - D.Sxx[i0]; sxy = Sxy[i1 + 1] - Sxy[i0]
    return (sxy - sx * sy / m) / (sxx - sx * sx / m)


def cums(D: Design, y: np.ndarray):
    return np.concatenate([[0.0], np.cumsum(y)]), np.concatenate([[0.0], np.cumsum(D.xc * y)])


def rolling(D: Design, Sy, Sxy, L: int, ends: np.ndarray) -> np.ndarray:
    return slopes_window(D, Sy, Sxy, D.roll_start[L][ends], ends)


def expanding(D: Design, Sy, Sxy, ends: np.ndarray, start: int = 0) -> np.ndarray:
    return slopes_window(D, Sy, Sxy, np.full(len(ends), start), ends)


def curvature_delta(D: Design, y: np.ndarray) -> float:
    """Implied change in the local exponent across the sample from a quadratic in ln t.
    With y = a + b*xc + c*xc^2, the local exponent is b + 2c*xc, so the change from the
    first to the last observation is 2c*(x_last - x_first). Negative = decline."""
    c = float(D.w_quad @ y)
    return 2.0 * c * D.x_span


# ------------------------------------------------------- HAC (Newey-West) ---
def nw_se_slope(xc: np.ndarray, resid: np.ndarray, lags: int) -> float:
    """Newey-West (Bartlett) SE of the slope, no small-sample correction
    (identical to statsmodels cov_hac(use_correction=False), verified in 01_reproduce)."""
    n = len(xc)
    X = np.column_stack([np.ones(n), xc])
    XtX_inv = np.linalg.inv(X.T @ X)
    g = X * resid[:, None]
    S = g.T @ g
    # autocovariances via FFT for speed
    f = np.fft.rfft(g, n=2 * n, axis=0)
    ac = np.fft.irfft(f[:, :, None] * np.conj(f[:, None, :]), n=2 * n, axis=0)[: lags + 1]
    # ac[k, i, j] = sum_t g[t+k, i] g[t, j]  (cross-correlation)
    for k in range(1, lags + 1):
        w = 1.0 - k / (lags + 1.0)
        Gk = ac[k]
        S += w * (Gk + Gk.T)
    V = XtX_inv @ S @ XtX_inv
    return float(math.sqrt(V[1, 1]))


# ------------------------------------------------------ break detector -----
def make_detector(xm: np.ndarray, min_len: int = 12, max_breaks: int = 4):
    """Exact dynamic-programming piecewise regression with BIC selection.
    Vectorized reimplementation of the v0.8 repository detector (same segments,
    same BIC: n*log(SSE/n) + 2*S*log(n)); equality is checked in 01_reproduce."""
    n = len(xm)
    sx = np.concatenate([[0.0], np.cumsum(xm)]); sxx = np.concatenate([[0.0], np.cumsum(xm * xm)])
    I, J = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    valid = (J - I + 1) >= min_len
    nn = np.where(valid, J - I + 1, 1).astype(float)
    X = sx[J + 1] - sx[I]; XX = sxx[J + 1] - sxx[I]
    den = np.where(valid, XX - X * X / nn, 1.0)

    def detect(y: np.ndarray) -> dict:
        sy = np.concatenate([[0.0], np.cumsum(y)]); syy = np.concatenate([[0.0], np.cumsum(y * y)])
        sxy = np.concatenate([[0.0], np.cumsum(xm * y)])
        Y = sy[J + 1] - sy[I]; YY = syy[J + 1] - syy[I]; XY = sxy[J + 1] - sxy[I]
        b = (XY - X * Y / nn) / den
        a = (Y - b * X) / nn
        sse = YY + a * a * nn + b * b * XX + 2 * a * b * X - 2 * a * Y - 2 * b * XY
        cost = np.where(valid, sse, np.inf)
        best = None
        dp_prev = np.full(n, np.inf); dp_prev[min_len - 1:] = cost[0, min_len - 1:]
        back = [None]
        dps = [dp_prev]
        for S in range(2, max_breaks + 2):
            # dp[S][j] = min_k dp[S-1][k] + cost[k+1, j]
            M = dps[-1][:-1, None] + cost[1:, :]            # rows k=0..n-2, cols j
            kmin = np.argmin(M, axis=0)
            dpS = M[kmin, np.arange(n)]
            dps.append(dpS); back.append(kmin)
        for K in range(max_breaks + 1):
            S = K + 1
            sseS = dps[K][n - 1]
            if not np.isfinite(sseS):
                continue
            bic = n * math.log(sseS / n) + 2 * S * math.log(n)
            if best is None or bic < best[0]:
                best = (bic, K)
        K = best[1]; S = K + 1
        ends = [n - 1]; j = n - 1
        for s in range(S, 1, -1):
            j = int(back[s - 1][j]); ends.append(j)
        ends = sorted(ends); starts = [0] + [e + 1 for e in ends[:-1]]
        slopes = np.array([b[i, j] for i, j in zip(starts, ends)])
        return {"K": K, "starts": starts, "slopes": slopes,
                "max_adj": float(np.max(np.abs(np.diff(slopes)))) if S > 1 else 0.0,
                "range": float(np.ptp(slopes))}
    return detect
