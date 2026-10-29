#!/usr/bin/env python3
"""Step 6: is the compression of cycle highs, with lows roughly unchanged,
distinguishable from symmetric shrinkage of persistent deviations?

Statistics (computed identically on the real series and every simulated path):
  Quantile regression of ln P on ln t at tau = 0.05, 0.50, 0.95 (statsmodels QuantReg).
    U  = b95 - b50      (upper-envelope slope relative to the median)
    Lw = b05 - b50      (lower-envelope slope relative to the median)
    Aq = U + Lw         symmetric shrinkage gives Aq ~ 0; top-only compression gives Aq < 0
  Halving-epoch extremes of the constant-B OLS residuals (epochs fixed by halving dates):
    sM, sm = least-squares slopes of epoch maxima and minima across epochs
    Aep = sM + sm       symmetric shrinkage gives Aep ~ 0; top-only compression gives Aep < 0
    computed for complete epochs E1-E3 (primary), E0-E3 (adds the partial first epoch)
    and E0-E4 (adds the incomplete current epoch; its maximum is a lower bound).

Null designs, for every plausible model:
  symmetric : the Gaussian deviation path as simulated (shrinking when lam > 0)
  skewed    : the same path, standardized by its rolling 4-year SD, rank-mapped onto the
              observed standardized-residual distribution (skewness +0.47), then rescaled by
              the same rolling SD and to the observed residual SD. This keeps the path's
              timing and persistence but gives it Bitcoin's right skew in constant proportion,
              so absolute compression is larger at the top than at the bottom by construction.

Writes outputs/asymmetry.csv and outputs/asymmetry_observed.json.
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
from lib import config as C                                           # noqa: E402
from lib.core import load_data, design_from_df                        # noqa: E402
from lib.nulls import Generator, main_family, seed_for                # noqa: E402

warnings.filterwarnings("ignore")
_G = {}
WIN = 1461


def roll_sd(u):
    return pd.Series(u).rolling(WIN, center=True, min_periods=500).std().bfill().ffill().to_numpy()


def _init(csv, allow):
    import statsmodels.api as sm
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float))
    X1 = np.column_stack([np.ones(D.n), D.xc])
    e = y - X1 @ (D.P1 @ y); resid_sd = float(np.std(e, ddof=1))
    z_obs = np.sort(e / roll_sd(e))
    _G.update(D=D, X1=X1, sm=sm, gen=Generator(df, resid_sd, D.x), z_obs=z_obs, resid_sd=resid_sd)


def stats(y):
    D, X1, sm = _G["D"], _G["X1"], _G["sm"]
    q = {t: sm.QuantReg(y, X1).fit(q=t, max_iter=5000).params[1] for t in (0.05, 0.5, 0.95)}
    e = y - X1 @ (D.P1 @ y)
    M = np.array([e[a:b].max() for a, b in D.epochs]); m = np.array([e[a:b].min() for a, b in D.epochs])
    def sl(v, idx):
        i = np.array(idx, float); return float(np.polyfit(i, v[idx], 1)[0])
    out = {"U": q[0.95] - q[0.5], "Lw": q[0.05] - q[0.5], "Aq": q[0.95] + q[0.05] - 2 * q[0.5]}
    for tag, idx in [("E1_3", [1, 2, 3]), ("E0_3", [0, 1, 2, 3]), ("E0_4", [0, 1, 2, 3, 4])]:
        sM, sm_ = sl(M, idx), sl(m, idx)
        out[f"sM_{tag}"] = sM; out[f"sm_{tag}"] = sm_; out[f"Aep_{tag}"] = sM + sm_
    return out


def skewed(u):
    s = roll_sd(u); z = u / s
    zm = _G["z_obs"][np.argsort(np.argsort(z))] if len(z) == len(_G["z_obs"]) else z
    v = zm * s
    D, X1 = _G["D"], _G["X1"]
    r = v - X1 @ (D.P1 @ v)
    return v * (_G["resid_sd"] / np.std(r, ddof=1))


def run(args):
    k, m, n_paths = args
    D, gen = _G["D"], _G["gen"]
    rng = np.random.default_rng(seed_for("asym", k))
    rows = []
    for _ in range(n_paths):
        u = gen.draw(m, rng)
        for variant, uu in (("symmetric", u), ("skewed", skewed(u))):
            s = stats(C.B_FULL_V08 * D.x + uu); s["variant"] = variant; rows.append(s)
    return m.id, pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--n", type=int, default=C.N_ASYM); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    out = ROOT / "outputs"
    _init(a.csv, a.allow_different_sample)
    df = load_data(Path(a.csv), require_frozen=not a.allow_different_sample)
    obs = stats(np.log(df.price_usd.to_numpy(float)))
    (out / "asymmetry_observed.json").write_text(json.dumps({k: round(v, 4) for k, v in obs.items()}, indent=2) + "\n")
    plaus = json.loads((out / "plausible_models.json").read_text())["plausible"]
    fam = {m.id: m for m in main_family()}
    jobs = [(i, fam[mid], a.n) for i, mid in enumerate(plaus)]
    t0 = time.time(); rows = []
    # every statistic is oriented so that SMALL values indicate top-only compression
    # (U, sM more negative; Lw, sm closer to zero instead of positive; Aq, Aep negative)
    lower = list(obs)
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for mid, R in pool.imap_unordered(run, jobs):
            print(f"{mid:28s} {time.time()-t0:6.0f}s", flush=True)
            for variant, G in R.groupby("variant"):
                N = len(G)
                for k in obs:
                    v = G[k].to_numpy()
                    p_lo = (v <= obs[k]).mean(); p_hi = (v >= obs[k]).mean()
                    rows.append({"model": mid, "variant": variant, "stat": k, "observed": obs[k],
                                 "null_mean": v.mean(), "null_sd": v.std(ddof=1),
                                 "p_lower": p_lo, "p_upper": p_hi,
                                 "p_directional": p_lo if k in lower else p_hi, "n": N})
    order = {m.id: i for i, m, _ in jobs}                       # job order, not completion order
    T = pd.DataFrame(rows).sort_values("model", key=lambda s: s.map(order), kind="mergesort")
    T.to_csv(out / "asymmetry.csv", index=False, float_format="%.4f")
    pd.set_option("display.width", 200)
    print(json.dumps({k: round(v, 3) for k, v in obs.items()}))
    print(T.pivot_table(index=["stat"], columns="variant", values="p_directional", aggfunc=["min", "median", "max"]).round(3).to_string())
    print(f"total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
