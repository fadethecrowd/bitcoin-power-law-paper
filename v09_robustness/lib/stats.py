"""The declared test battery and the residual features used to screen null models.

compute(y) returns scalar statistics plus a few short vectors (rolling and
expanding paths at month-ends, start-date exponents) that are only ever used
to form aggregate null bands; they are never written out per path.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import skew

from . import config as C
from .core import Design, cums, rolling, expanding, curvature_delta, slopes_window

# Direction in which each statistic would move under a declining exponent.
# "lo": small values are evidence of decline; "hi": large values; None: two-sided/variability.
DIRECTION = {
    "d17": "lo", "curv": "lo", "mean5": "lo", "r5_2025": "lo",
    **{f"rmin{L}": "lo" for L in C.ROLL_YEARS},
    **{f"rend{L}": "lo" for L in C.ROLL_YEARS},
    "exp_drop": "hi",
    "brk_maxadj": "hi", "brk_range": "hi",
    **{f"rsd{L}": "hi" for L in C.ROLL_YEARS},
    "exp_range": "hi",
}
# The selection-aware battery: directional statistics that were examined after the
# historical data had been seen (October 2026 reviews). Their joint null distribution
# is used for a max-T (min-p) adjustment.
BATTERY = ["d17", "curv", "mean5", "r5_2025", "rmin5", "exp_drop"]

FEATURES = ["acf1", "acf365", "acf1461", "zero_cross", "amp_ratio", "dvol_ratio", "band_share"]


class Battery:
    def __init__(self, D: Design, detector):
        self.D = D
        self.detect = detector
        d = D.dates
        self.first5 = np.flatnonzero(d < d[0] + np.timedelta64(int(5 * 365.25), "D"))
        self.last5 = np.flatnonzero(d > d[-1] - np.timedelta64(int(5 * 365.25), "D"))
        self.first4 = np.flatnonzero(d < d[0] + np.timedelta64(int(4 * 365.25), "D"))
        self.last4 = np.flatnonzero(d > d[-1] - np.timedelta64(int(4 * 365.25), "D"))
        n = D.n
        freqs = np.fft.rfftfreq(n, d=1.0)                       # cycles per day
        self.band = (freqs >= 1 / (5 * 365.25)) & (freqs <= 1 / (3 * 365.25))
        self.i2025 = C.NAMED_ENDS.index("2025-12-31")

    # -------------------------------------------------------------- battery --
    def compute(self, y: np.ndarray, with_features: bool = True, with_breaks: bool = True) -> dict:
        D = self.D
        Sy, Sxy = cums(D, y)
        n = D.n
        full = float(slopes_window(D, Sy, Sxy, np.array([0]), np.array([n - 1]))[0])
        post = float(slopes_window(D, Sy, Sxy, np.array([D.i_post]), np.array([n - 1]))[0])
        out = {"full": full, "post17": post, "d17": post - full, "curv": curvature_delta(D, y)}
        vec = {}
        for L in C.ROLL_YEARS:
            path = rolling(D, Sy, Sxy, L, D.roll_eval[L])
            named = rolling(D, Sy, Sxy, L, D.named)
            out[f"rmin{L}"] = float(path.min()); out[f"rmax{L}"] = float(path.max())
            out[f"rsd{L}"] = float(path.std()); out[f"rend{L}"] = float(path[-1])
            out[f"r{L}_2025"] = float(named[self.i2025])
            if L == 5:
                out["mean5"] = float(named[1:].mean())
                vec["roll5"] = path
                vec["roll5_named"] = named
            vec[f"roll{L}"] = path
        out["r5_2025"] = out["r5_2025"]
        ex = expanding(D, Sy, Sxy, D.exp_eval)
        out["exp_range"] = float(ex.max() - ex.min()); out["exp_drop"] = float(ex.max() - ex[-1])
        vec["exp"] = expanding(D, Sy, Sxy, D.month_end[D.month_end >= 365])
        vec["exp17"] = expanding(D, Sy, Sxy, D.month_end[D.month_end >= D.i_post + 365], start=D.i_post)
        vec["start_B"] = slopes_window(D, Sy, Sxy, D.year_start_idx, np.full(len(D.year_start_idx), n - 1))
        if with_breaks:
            r = self.detect(y[D.monthly])
            out["brk_K"] = r["K"]; out["brk_maxadj"] = r["max_adj"]; out["brk_range"] = r["range"]
        if with_features:
            out.update(self.features(y))
        return out, vec

    # ------------------------------------------------------------- features --
    def residuals(self, y: np.ndarray) -> np.ndarray:
        X1 = np.column_stack([np.ones(self.D.n), self.D.xc])
        return y - X1 @ (self.D.P1 @ y)

    def features(self, y: np.ndarray) -> dict:
        e = self.residuals(y)
        v = float(np.dot(e, e))
        acf = lambda k: float(np.dot(e[:-k], e[k:]) / v)
        de = np.diff(e)
        P = np.abs(np.fft.rfft(e)) ** 2
        return {
            "acf1": acf(1), "acf365": acf(365), "acf1461": acf(1461),
            "zero_cross": int(np.count_nonzero(np.diff(np.sign(e)) != 0)),
            "amp_ratio": float(e[self.last5].std() / e[self.first5].std()),
            "dvol_ratio": float(de[self.last4[:-1]].std() / de[self.first4[:-1]].std()),
            "band_share": float(P[self.band].sum() / P[1:].sum()),
            "skew": float(skew(e)),
        }
