#!/usr/bin/env python3
"""Step 8: cross-check this simulator against published Baquero & Menezes (Oct 2026) numbers.

Their replication package (Zenodo 23218897) could not be retrieved from this
environment, so the comparison is against figures printed in the paper:

  Fig. 1b: histories with CONSTANT DRIFT in log price (no log-age term) plus
           random-walk deviations with Bitcoin's volatility profile, fitted by
           OLS of ln P on ln t: median R^2 0.897 (90% range 0.70-0.97); fitted
           exponents median 6.1 (90% range 3.4-9.2). (Weekly, 2011-2026.)

We reproduce the design on the daily frozen-sample grid: drift equal to the
observed mean daily log growth, random-walk deviations whose daily innovation SD
equals the observed annual SD of daily log returns (lambda = 1, unscaled).
Appendix G comparisons (Newey-West coverage, residual ADF) are in step 5.

Writes outputs/bm_crosscheck.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                       # noqa: E402
from lib.core import load_data, design_from_df                    # noqa: E402
from lib.nulls import Generator, seed_for                          # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--n", type=int, default=1000)
    a = ap.parse_args()
    df = load_data(Path(a.csv), require_frozen=not a.allow_different_sample)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float))
    gen = Generator(df, 1.0, D.x)
    t = D.t
    g = (y[-1] - y[0]) / (t[-1] - t[0])                      # mean daily log growth
    sig = gen.h                                                # unnormalized daily return SD by year
    X1 = np.column_stack([np.ones(D.n), D.xc])
    rng = np.random.default_rng(np.random.SeedSequence([C.MASTER_SEED, 8]))
    B, R2 = [], []
    obs_r2 = None
    for _ in range(a.n):
        e = rng.standard_normal(gen.N) * sig
        u = np.cumsum(e)[gen.keep]
        yy = y[0] + g * (t - t[0]) + (u - u[0])
        beta = D.P1 @ yy; r = yy - X1 @ beta
        B.append(beta[1]); R2.append(1 - r.var() / yy.var())
    B = np.array(B); R2 = np.array(R2)
    beta = D.P1 @ y; r = y - X1 @ beta; obs_r2 = 1 - r.var() / y.var()
    out = {"design": "constant drift + random-walk deviations with observed volatility profile; daily frozen grid",
           "n_sims": a.n, "drift_per_day": round(float(g), 6),
           "fitted_B_median": round(float(np.median(B)), 3),
           "fitted_B_90pct": [round(float(v), 3) for v in np.quantile(B, [0.05, 0.95])],
           "R2_median": round(float(np.median(R2)), 3),
           "R2_90pct": [round(float(v), 3) for v in np.quantile(R2, [0.05, 0.95])],
           "share_R2_above_observed": round(float((R2 > obs_r2).mean()), 3), "observed_R2": round(float(obs_r2), 4),
           "baquero_menezes_fig1b": {"R2_median": 0.897, "R2_90pct": [0.70, 0.97], "share_above_bitcoin": 0.14,
                                     "B_median": 6.1, "B_90pct": [3.4, 9.2], "sample": "weekly, 2011-2026"}}
    (ROOT / "outputs" / "bm_crosscheck.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
