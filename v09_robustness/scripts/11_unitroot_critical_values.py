#!/usr/bin/env python3
"""Step 11: critical values for unit-root tests on residuals from ln P = a + B ln t.

The residual is taken from a regression on a constant and the *deterministic*
regressor ln t. Neither the Dickey-Fuller constant-only tables (ln t is a
fitted trend) nor the Engle-Granger / Phillips-Ouliaris cointegration tables
(ln t is not an I(1) regressor) are exact for this design, so the null
distribution is simulated directly:

  * H0 deviation u_t is a random walk on the daily calendar from genesis,
    sampled on the observed days, either with constant innovation variance
    (lam = 0, the textbook null) or with Bitcoin's annual volatility profile
    (lam = 1);
  * y = B ln t + u is regressed on (1, ln t) exactly as the real series is;
  * the residual ADF t-statistic (constant; fixed lags 1, 5, 10, 21, 33 and AIC
    up to 33, statsmodels) and the Phillips-Perron Z_t (constant, Bartlett,
    lag 11 and automatic lag, arch) are recorded.

Reports the 1%, 5% and 10% quantiles with the Phillips-Ouliaris (1990) /
MacKinnon (2010) residual-based values and the real-series statistics.
Writes outputs/unitroot_critical_values.csv.
"""
from __future__ import annotations

import argparse
import json
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
from lib.core import load_data, design_from_df                         # noqa: E402
from lib.nulls import Generator, Model, seed_for                       # noqa: E402

warnings.filterwarnings("ignore")
ADF_LAGS = [1, 5, 10, 21, 33]
N_REPS = 2000
_G = {}


def _init(csv, allow):
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float))
    X1 = np.column_stack([np.ones(D.n), D.xc]); resid_sd = float(np.std(y - X1 @ (D.P1 @ y), ddof=1))
    _G.update(D=D, X1=X1, gen=Generator(df, resid_sd, D.x), y=y)


def stats_for(e):
    from statsmodels.tsa.stattools import adfuller
    from arch.unitroot import PhillipsPerron
    r = {f"adf{L}": adfuller(e, maxlag=L, regression="c", autolag=None)[0] for L in ADF_LAGS}
    r["adf_aic"] = adfuller(e, maxlag=33, regression="c", autolag="AIC")[0]
    r["pp11"] = PhillipsPerron(e, lags=11, trend="c").stat
    r["pp_auto"] = PhillipsPerron(e, trend="c").stat
    return r


def run(args):
    k, lam, n = args
    D, X1, gen = _G["D"], _G["X1"], _G["gen"]
    m = Model("rw", "rw", 1.0, 0.0, lam)
    rng = np.random.default_rng(seed_for("critval", k))
    rows = []
    for _ in range(n):
        y = C.B_FULL_V08 * D.x + gen.draw(m, rng)
        e = y - X1 @ (D.P1 @ y)
        rows.append(stats_for(e))
    return lam, pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--workers", type=int, default=2); ap.add_argument("--n", type=int, default=N_REPS)
    a = ap.parse_args()
    _init(a.csv, a.allow_different_sample)
    e_obs = _G["y"] - _G["X1"] @ (_G["D"].P1 @ _G["y"])
    obs = stats_for(e_obs)
    jobs = [(0, 0.0, a.n), (1, 1.0, a.n)]
    t0 = time.time(); res = {}
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for lam, S in pool.imap_unordered(run, jobs):
            res[lam] = S; print(f"lam={lam:g} done {time.time()-t0:.0f}s", flush=True)
    rows = []
    for stat in obs:
        row = {"statistic": stat, "observed": obs[stat]}
        for lam, tag in [(0.0, "const_vol"), (1.0, "btc_vol")]:
            q = np.quantile(res[lam][stat], [0.01, 0.05, 0.10])
            row.update({f"{tag}_1pct": q[0], f"{tag}_5pct": q[1], f"{tag}_10pct": q[2],
                        f"{tag}_p": float((res[lam][stat] <= obs[stat]).mean())})
        row.update({"PO1990_5pct": -3.37, "MacKinnon2010_5pct": -3.337, "DF_const_5pct": -2.862})
        rows.append(row)
    T = pd.DataFrame(rows)
    T.to_csv(ROOT / "outputs" / "unitroot_critical_values.csv", index=False, float_format="%.4f")
    pd.set_option("display.width", 220)
    print(T.round(3).to_string(index=False))
    print(json.dumps({"n_reps": a.n, "seed_stage": C.STAGE["critval"]}))


if __name__ == "__main__":
    main()
