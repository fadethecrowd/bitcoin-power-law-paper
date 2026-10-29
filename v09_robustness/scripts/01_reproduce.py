#!/usr/bin/env python3
"""Step 1: deterministic reproduction on the real series.

Reproduces the v0.8 baseline, the post-2017, expanding and rolling exponents,
the window-length and start-date tables, the 2025 departing-versus-arriving
decomposition, the residual unit-root diagnostics, quantile slopes and
halving-epoch residual extremes. Also checks that the fast estimators in
lib/core.py agree exactly with the v0.8 reference implementations.

Writes outputs/reproduction.json (aggregate values only).
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                      # noqa: E402
from lib.core import (load_data, design_from_df, sha256, cums, rolling, expanding,   # noqa: E402
                      slopes_window, curvature_delta, nw_se_slope, make_detector)
from lib.reference import detector_factory_v08, moving_block_bootstrap_v08   # noqa: E402
from lib.stats import Battery                                    # noqa: E402

warnings.filterwarnings("ignore")
R = lambda v, k=6: None if v is None else round(float(v), k)


def decomposition(df, D, y, year_end_prev, year_end):
    """Daily-path attribution of the change in rolling-5y B over one year.
    Each day's change is split between observations leaving and entering the window,
    averaging the two orders (Shapley). Also reports the two single-step orders."""
    dt = df.date
    x = D.xc
    def win(e):
        e = pd.Timestamp(e); return np.flatnonzero(((dt > e - pd.DateOffset(years=5)) & (dt <= e)).to_numpy())
    def b(ix):
        xx = x[ix]; yy = y[ix]; xm = xx.mean(); return float(np.dot(xx - xm, yy - yy.mean()) / np.dot(xx - xm, xx - xm))
    W0 = win(year_end_prev); W1 = win(year_end)
    drop = np.setdiff1d(W0, W1); add = np.setdiff1d(W1, W0)
    b0, b1 = b(W0), b(W1)
    bC = b(np.intersect1d(W0, W1)); bU = b(np.union1d(W0, W1))
    prev = W0; tot_d = tot_a = 0.0
    for e in pd.date_range(pd.Timestamp(year_end_prev) + pd.Timedelta(days=1), year_end):
        cur = win(e); dr = np.setdiff1d(prev, cur); ad = np.setdiff1d(cur, prev)
        bp = b(prev); bc = b(cur)
        bd = b(np.setdiff1d(prev, dr)) if len(dr) else bp
        ba = b(np.union1d(prev, ad))
        tot_d += 0.5 * ((bd - bp) + (bc - ba)); tot_a += 0.5 * ((ba - bp) + (bc - bd)); prev = cur
    return {"from": year_end_prev, "to": year_end, "B_from": R(b0, 4), "B_to": R(b1, 4), "dB": R(b1 - b0, 4),
            "daily_shapley_departing": R(tot_d, 4), "daily_shapley_arriving": R(tot_a, 4),
            "two_step_drop_first": {"departing": R(bC - b0, 4), "arriving": R(b1 - bC, 4)},
            "two_step_add_first": {"arriving": R(bU - b0, 4), "departing": R(b1 - bU, 4)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT / "outputs")
    a = ap.parse_args()
    df = load_data(a.csv, require_frozen=not a.allow_different_sample)
    D = design_from_df(df)
    y = np.log(df.price_usd.to_numpy(float))
    out = {"input_sha256": sha256(a.csv), "frozen_match": sha256(a.csv) == C.FROZEN_SHA256,
           "n": D.n, "first": str(D.dates[0].date()), "last": str(D.dates[-1].date())}

    # ---- baseline and HAC (statsmodels, v0.8 convention) and fast-NW agreement
    X = sm.add_constant(D.x)
    res = sm.OLS(y, X).fit()
    e = np.asarray(res.resid)
    hac = float(np.sqrt(cov_hac(res, nlags=365, use_correction=False)[1, 1]))
    fast = nw_se_slope(D.xc, e, 365)
    out["baseline"] = {"B": R(res.params[1], 9), "A": float(np.exp(res.params[0])), "R2": R(res.rsquared, 9),
                       "residual_sd": R(np.std(e, ddof=1), 9), "lag1_acf_pearson": R(np.corrcoef(e[:-1], e[1:])[0, 1], 9),
                       "naive_se": R(res.bse[1], 9), "hac365_se": R(hac, 9),
                       "fast_nw_matches_statsmodels": bool(abs(fast - hac) < 1e-9),
                       "hac1461_se": R(nw_se_slope(D.xc, e, 1461), 6),
                       "v08_target_B": C.B_FULL_V08}
    # ---- post-2017, expanding at v0.8 dates, rolling at named dates
    Sy, Sxy = cums(D, y)
    n = D.n
    out["post2017_B"] = R(slopes_window(D, Sy, Sxy, np.array([D.i_post]), np.array([n - 1]))[0])
    v08_dates = ["2016-12-31", "2018-12-31", "2020-12-31", "2021-12-31", "2022-12-31", "2023-12-31",
                 "2024-12-31", "2025-12-31", "2026-08-14"]
    ex_idx = np.array([D.idx[pd.Timestamp(s)] for s in v08_dates])
    out["expanding_B"] = {s: R(v) for s, v in zip(v08_dates, expanding(D, Sy, Sxy, ex_idx))}
    exm = expanding(D, Sy, Sxy, D.exp_eval)
    full_daily_exp = expanding(D, Sy, Sxy, np.arange(D.i_post, n))
    k = int(np.argmax(full_daily_exp))
    out["expanding_since_2017"] = {"month_end_range": R(exm.max() - exm.min(), 4),
                                   "daily_max": R(full_daily_exp[k], 4), "daily_max_date": str(D.dates[D.i_post + k].date()),
                                   "drop_from_daily_max": R(full_daily_exp[k] - full_daily_exp[-1], 4)}
    roll = {}
    for L in C.ROLL_YEARS:
        named = rolling(D, Sy, Sxy, L, D.named)
        daily = rolling(D, Sy, Sxy, L, np.arange(D.roll_eval[L][0], n))
        i_lo, i_hi = int(np.argmin(daily)), int(np.argmax(daily))
        roll[f"{L}y"] = {"named": {s: R(v, 4) for s, v in zip(C.NAMED_ENDS, named)},
                         "daily_min": R(daily[i_lo], 4), "daily_min_date": str(D.dates[D.roll_eval[L][0] + i_lo].date()),
                         "daily_max": R(daily[i_hi], 4), "daily_max_date": str(D.dates[D.roll_eval[L][0] + i_hi].date()),
                         "month_end_sd": R(rolling(D, Sy, Sxy, L, D.roll_eval[L]).std(), 4)}
    out["rolling_B"] = roll
    # ---- start-date sensitivity (fixed end dates)
    starts = ["2010-07-17"] + C.YEAR_STARTS
    sidx = np.array([D.idx[pd.Timestamp(s)] for s in starts])
    tab = {}
    for end in ["2025-12-31", "2026-08-14"]:
        ei = D.idx[pd.Timestamp(end)]
        tab[end] = {s: R(v, 4) for s, v in zip(starts, slopes_window(D, Sy, Sxy, sidx, np.full(len(sidx), ei)))}
    out["start_date_B"] = tab
    # ---- curvature and the October 2026 battery values
    B = Battery(D, make_detector(np.log(df.days_since_genesis.to_numpy(float))[D.monthly]))
    stats, _ = B.compute(y)
    out["battery_observed"] = {k: R(v, 6) for k, v in stats.items()}
    out["curvature_quadratic_coef_ln"] = R(float(D.w_quad @ y), 6)
    # ---- detector agreement with the v0.8 reference implementation
    xm = D.x[D.monthly]; ym = y[D.monthly]
    ref = detector_factory_v08(xm)(ym); fst = make_detector(xm)(ym)
    rng = np.random.default_rng(7)
    agree = ref["K"] == fst["K"] and np.allclose(ref["slopes"], fst["slopes"])
    for _ in range(10):
        ys = 5.65 * xm + np.cumsum(rng.standard_normal(len(xm))) * 0.2
        r1 = detector_factory_v08(xm)(ys); r2 = make_detector(xm)(ys)
        agree &= r1["K"] == r2["K"] and np.allclose(r1["slopes"], r2["slopes"])
    out["break_detector"] = {"monthly_n": int(len(xm)), "selected_K": int(ref["K"]),
                             "break_dates": [str(D.dates[D.monthly[s]].date()) for s in ref["starts"][1:]],
                             "segment_slopes": [R(s, 3) for s in ref["slopes"]],
                             "max_adjacent_slope_change": R(ref["max_adj"], 4), "slope_range": R(ref["range"], 4),
                             "fast_detector_matches_reference": bool(agree)}
    # ---- 2025 decomposition (and the other years, for the bridge)
    out["decomposition"] = [decomposition(df, D, y, a_, b_) for a_, b_ in
                            [("2021-12-31", "2022-12-31"), ("2022-12-31", "2023-12-31"), ("2023-12-31", "2024-12-31"),
                             ("2024-12-31", "2025-12-31"), ("2025-12-31", "2026-08-14")]]
    # ---- unit-root diagnostics on residuals (v0.8 conventions) and Phillips-Perron
    from arch.unitroot import PhillipsPerron
    adf = {str(L): R(adfuller(e, maxlag=L, regression="c", autolag=None)[0], 4) for L in [1, 5, 10, 21, 33]}
    adf_aic = adfuller(e, maxlag=33, regression="c", autolag="AIC")
    out["unit_root"] = {"adf_fixed_lags": adf, "adf_aic": {"stat": R(adf_aic[0], 4), "lags": int(adf_aic[2])},
                        "pp_lag11_const": R(PhillipsPerron(e, lags=11, trend="c").stat, 4),
                        "pp_auto_const": R(PhillipsPerron(e, trend="c").stat, 4),
                        "v08_reported_pp": -2.380,
                        "critical_values": {"DF_5pct": -2.86, "EG_residual_5pct": -3.37, "EG_residual_10pct": -3.07}}
    # ---- moving-block bootstrap (v0.8 repository algorithm and reconstruction seed)
    bs = moving_block_bootstrap_v08(D.x, y, 365, 1000, 20261001)
    out["block_bootstrap_365"] = {"seed": 20261001, "sd": R(bs.std(ddof=1), 4), "q025": R(np.quantile(bs, .025), 4),
                                  "q975": R(np.quantile(bs, .975), 4), "v08_audited_sd": 0.2401}
    # ---- quantile slopes and halving-epoch residual extremes
    q = {}
    for tau in [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]:
        q[str(tau)] = R(sm.QuantReg(y, X).fit(q=tau, max_iter=5000).params[1], 4)
    out["quantile_slopes"] = q
    ep = []
    for k_, (i0, i1) in enumerate(D.epochs):
        seg = e[i0:i1]
        # Data policy: an epoch extreme reported with its date and enough precision, combined with
        # the public A and B, approximates one day's licensed close. Public output therefore gives
        # each extreme rounded to 2 decimals (as printed in the paper) and without its date.
        ep.append({"epoch": f"E{k_}", "start": str(D.dates[i0].date()), "end": str(D.dates[i1 - 1].date()),
                   "complete": 0 < k_ < len(D.epochs) - 1,
                   "max_resid_ln": R(seg.max(), 2), "min_resid_ln": R(seg.min(), 2)})
    out["halving_epochs"] = ep
    out["observed_features"] = {k: R(v, 5) for k, v in B.features(y).items()}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "reproduction.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
