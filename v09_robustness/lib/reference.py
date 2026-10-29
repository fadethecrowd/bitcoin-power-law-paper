"""Reference implementations copied from the v0.8 public repository
(fadethecrowd/bitcoin-power-law-paper, scripts/stochastic_checks.py, commit 95b6a2a)
so that the fast versions in core.py can be checked for exact agreement."""
from __future__ import annotations

import math
import numpy as np


def detector_factory_v08(x, min_len=12, max_breaks=4):
    n = len(x); sx = np.r_[0, np.cumsum(x)]; sxx = np.r_[0, np.cumsum(x * x)]

    def detect(y):
        sy = np.r_[0, np.cumsum(y)]; syy = np.r_[0, np.cumsum(y * y)]; sxy = np.r_[0, np.cumsum(x * y)]
        cost = np.full((n, n), np.inf); slp = np.full((n, n), np.nan)
        for i in range(n):
            js = np.arange(i + min_len - 1, n)
            if len(js) == 0:
                continue
            nn = js - i + 1; X = sx[js + 1] - sx[i]; Y = sy[js + 1] - sy[i]; XX = sxx[js + 1] - sxx[i]
            YY = syy[js + 1] - syy[i]; XY = sxy[js + 1] - sxy[i]
            den = XX - X * X / nn; b = (XY - X * Y / nn) / den; a = (Y - b * X) / nn
            sse = YY + a * a * nn + b * b * XX + 2 * a * b * X - 2 * a * Y - 2 * b * XY
            cost[i, js] = sse; slp[i, js] = b
        candidates = []
        for K in range(max_breaks + 1):
            S = K + 1; dp = np.full((S + 1, n), np.inf); prev = np.full((S + 1, n), -1, int)
            dp[1, min_len - 1:] = cost[0, min_len - 1:]
            for s in range(2, S + 1):
                for j in range(s * min_len - 1, n):
                    ks = np.arange((s - 1) * min_len - 1, j - min_len + 1)
                    vals = dp[s - 1, ks] + cost[ks + 1, j]
                    q = int(np.argmin(vals)); dp[s, j] = vals[q]; prev[s, j] = int(ks[q])
            sse = dp[S, n - 1]
            bic = n * math.log(sse / n) + (2 * S) * math.log(n)
            ends = [n - 1]; jj = n - 1
            for s in range(S, 1, -1):
                jj = prev[s, jj]; ends.append(jj)
            ends = sorted(ends); starts = [0] + [e + 1 for e in ends[:-1]]
            slopes = np.array([slp[i, j] for i, j in zip(starts, ends)])
            candidates.append((bic, K, starts, ends, slopes))
        bic, K, starts, ends, slopes = min(candidates, key=lambda z: z[0])
        return {"K": K, "starts": starts, "slopes": slopes,
                "max_adj": float(np.max(np.abs(np.diff(slopes)))) if len(slopes) > 1 else 0.0,
                "range": float(np.ptp(slopes))}
    return detect


def moving_block_bootstrap_v08(x, y, block_days=365, reps=1000, seed=20261001):
    """v0.8 repository moving-block bootstrap of (ln t, ln P) pairs."""
    n = len(x); rng = np.random.default_rng(seed)
    starts_max = n - block_days + 1; nblocks = math.ceil(n / block_days)
    offsets = np.arange(block_days); vals = np.empty(reps)
    for b in range(reps):
        starts = rng.integers(0, starts_max, size=nblocks)
        idx = np.concatenate([s + offsets for s in starts])[:n]
        xc = x[idx] - x[idx].mean(); yc = y[idx] - y[idx].mean()
        vals[b] = np.dot(xc, yc) / np.dot(xc, xc)
    return vals
