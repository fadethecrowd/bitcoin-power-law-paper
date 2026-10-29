#!/usr/bin/env python3
"""Step 5: do the v0.8 uncertainty intervals and unit-root diagnostics behave as
advertised when the residual process is a member of the declared family?

For each model, N_HAC constant-B histories are drawn and we record
  * coverage of the true B by  B_hat +/- 1.96 * NW SE  (Bartlett, lag 365 as in v0.8, and lag 1,461)
  * coverage by the 365-day moving-block-bootstrap percentile interval (v0.8 algorithm, BOOT_REPS draws)
  * the true sampling SD of B_hat versus the average NW SE and bootstrap SD
  * rejection rates of residual ADF (v0.8 fixed lags; AIC lag) and Phillips-Perron (lag 11)
    at the ordinary Dickey-Fuller 5% value (-2.86) and the residual-based Engle-Granger 5% value (-3.37).
Under random-walk deviations every rejection is a false positive; under AR deviations it is power.

Also re-runs the v0.8 AR(1) equal-standardized-gap illustration (a mathematical result
conditional on a stationary AR(1); nothing in this study tests or contradicts it).

Writes outputs/hac_coverage.csv, outputs/unitroot.csv, outputs/scale_invariance.json.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                            # noqa: E402
from lib.core import load_data, design_from_df, nw_se_slope             # noqa: E402
from lib.nulls import Generator, Model, main_family, seed_for            # noqa: E402

warnings.filterwarnings("ignore")
EXTRA = ["rw|cyc0.0|lam1", "rw|cyc0.0|lam0", "ar0.997|cyc0.0|lam0", "ar0.990|cyc0.0|lam0"]
ADF_LAGS = [1, 5, 10, 21, 33]
DF5, EG5 = -2.86, -3.37
_G = {}


def _init(csv, allow):
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float))
    X1 = np.column_stack([np.ones(D.n), D.xc]); resid_sd = float(np.std(y - X1 @ (D.P1 @ y), ddof=1))
    n = D.n; L = 365
    nb = math.ceil(n / L); tail = n - (nb - 1) * L
    _G.update(D=D, gen=Generator(df, resid_sd, D.x), X1=X1, L=L, nb=nb, tail=tail)


def boot_slopes(x, y, rng, reps):
    """v0.8 moving-block bootstrap (365-day blocks, blocks concatenated and truncated to n),
    evaluated with block sums so each replicate costs O(number of blocks)."""
    L, nb, tail = _G["L"], _G["nb"], _G["tail"]
    n = len(x)
    c = lambda v: np.concatenate([[0.0], np.cumsum(v)])
    cx, cy, cxx, cxy = c(x), c(y), c(x * x), c(x * y)
    smax = n - L + 1
    st = rng.integers(0, smax, size=(reps, nb))
    full, last = st[:, :-1], st[:, -1]
    def s(cs):
        return (cs[full + L] - cs[full]).sum(1) + (cs[last + tail] - cs[last])
    Sx, Sy, Sxx, Sxy = s(cx), s(cy), s(cxx), s(cxy)
    return (Sxy - Sx * Sy / n) / (Sxx - Sx * Sx / n)


def run(args):
    from statsmodels.tsa.stattools import adfuller
    from arch.unitroot import PhillipsPerron
    k, m, n_paths = args
    D, gen, X1 = _G["D"], _G["gen"], _G["X1"]
    rng = np.random.default_rng(seed_for("hac", k))
    rows = []
    for _ in range(n_paths):
        u = gen.draw(m, rng)
        y = C.B_FULL_V08 * D.x + u
        beta = D.P1 @ y; e = y - X1 @ beta; b = beta[1]
        nw365 = nw_se_slope(D.xc, e, 365); nw1461 = nw_se_slope(D.xc, e, 1461)
        bs = boot_slopes(D.xc, y, rng, C.BOOT_REPS)
        lo, hi = np.quantile(bs, [0.025, 0.975])
        r = {"B_hat": b, "nw365": nw365, "nw1461": nw1461, "boot_sd": bs.std(ddof=1),
             "cov_nw365": abs(b - C.B_FULL_V08) <= 1.96 * nw365,
             "cov_nw1461": abs(b - C.B_FULL_V08) <= 1.96 * nw1461,
             "cov_boot": lo <= C.B_FULL_V08 <= hi}
        for L in ADF_LAGS:
            r[f"adf{L}"] = adfuller(e, maxlag=L, regression="c", autolag=None)[0]
        r["adf_aic"] = adfuller(e, maxlag=33, regression="c", autolag="AIC")[0]
        r["pp11"] = PhillipsPerron(e, lags=11, trend="c").stat
        rows.append(r)
    return m.id, pd.DataFrame(rows)


def ar1_demo(reps=4000, seed=20261001):
    """Re-run of the v0.8 / repository equal-standardized-gap illustration."""
    rho = 0.99699; sigmas = [0.85, 0.55, 0.31]
    def go(mode, sigma, off):
        rng = np.random.default_rng(seed + off)
        start = -0.82 if mode == "raw" else -2.0 * sigma
        x = np.full(reps, start); act = np.ones(reps, bool); tt = np.full(reps, np.nan)
        isd = sigma * math.sqrt(1 - rho * rho)
        for t in range(1, 10001):
            ii = np.flatnonzero(act)
            if not len(ii):
                break
            x[ii] = rho * x[ii] + rng.normal(0, isd, len(ii)); hit = x[ii] >= 0
            tt[ii[hit]] = t; act[ii[hit]] = False
        return float(np.nanmedian(tt))
    return {"rho": rho, "sigmas": sigmas, "reps": reps, "seed": seed,
            "median_days_same_raw_gap": [go("raw", s, 10 + i) for i, s in enumerate(sigmas)],
            "median_days_same_standardized_gap": [go("std", s, 110 + i) for i, s in enumerate(sigmas)],
            "v08_reported_standardized": [398, 393, 392]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--n", type=int, default=C.N_HAC); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    out = ROOT / "outputs"
    plaus = json.loads((out / "plausible_models.json").read_text())["plausible"]
    fam = {m.id: m for m in main_family()}
    ids = plaus + [e for e in EXTRA if e not in plaus]
    jobs = [(i, fam[mid], a.n) for i, mid in enumerate(ids)]
    t0 = time.time(); rows_cov, rows_ur = [], []
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for mid, R in pool.imap_unordered(run, jobs):
            print(f"{mid:28s} {time.time()-t0:6.0f}s", flush=True)
            N = len(R)
            rows_cov.append({"model": mid, "plausible": mid in plaus, "n": N,
                             "true_sd_B": R.B_hat.std(ddof=1), "mean_nw365": R.nw365.mean(),
                             "mean_nw1461": R.nw1461.mean(), "mean_boot_sd": R.boot_sd.mean(),
                             "ratio_true_to_nw365": R.B_hat.std(ddof=1) / R.nw365.mean(),
                             "cover_nw365": R.cov_nw365.mean(), "cover_nw1461": R.cov_nw1461.mean(),
                             "cover_boot365": R.cov_boot.mean(),
                             "mc_se_cover": math.sqrt(0.95 * 0.05 / N)})
            r = {"model": mid, "plausible": mid in plaus, "n": N,
                 "unit_root_true": fam[mid].kind == "rw"}
            for col in [f"adf{L}" for L in ADF_LAGS] + ["adf_aic", "pp11"]:
                r[f"{col}_rej_DF5"] = (R[col] < DF5).mean(); r[f"{col}_rej_EG5"] = (R[col] < EG5).mean()
            rows_ur.append(r)
    order = {mid: i for i, mid in enumerate(ids)}               # job order, not completion order
    cov = pd.DataFrame(rows_cov).sort_values("model", key=lambda s: s.map(order), kind="mergesort")
    ur = pd.DataFrame(rows_ur).sort_values("model", key=lambda s: s.map(order), kind="mergesort")
    cov.to_csv(out / "hac_coverage.csv", index=False, float_format="%.4f")
    ur.to_csv(out / "unitroot.csv", index=False, float_format="%.4f")
    demo = ar1_demo()
    (out / "scale_invariance.json").write_text(json.dumps(demo, indent=2) + "\n")
    pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
    print(cov.round(3).to_string(index=False)); print(ur.round(3).to_string(index=False)); print(demo)
    print(f"total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
