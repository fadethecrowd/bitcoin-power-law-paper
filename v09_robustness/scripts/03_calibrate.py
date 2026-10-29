#!/usr/bin/env python3
"""Step 3: screen the null family against the observed residuals and calibrate
every statistic in the battery under each model.

Screening (plausibility), using residual features that are NOT test statistics:
  lag-1, 365-day and 1,461-day autocorrelation; number of zero crossings;
  residual-amplitude ratio (last 5 years / first 5 years); share of residual
  variance at periods of 3-5 years.
A model is "plausible" if (i) its Mahalanobis p-value for the six features
jointly is >= 0.05 and (ii) every single-feature two-sided p-value is >= 0.01.
Models failing either rule are kept as "sensitivity extremes".

Writes outputs/screening.csv, plausible_models.json, calibration.csv,
calibration_summary.csv, maxT.csv, breaks_null.csv.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                         # noqa: E402
from lib.stats import DIRECTION, BATTERY            # noqa: E402

SCREEN = ["acf1", "acf365", "acf1461", "zero_cross", "amp_ratio", "band_share"]
REPORT_ONLY = ["dvol_ratio", "skew"]


def load(pattern):
    out = {}
    for f in sorted(glob.glob(str(ROOT / "cache" / pattern))):
        z = np.load(f)
        m = json.loads(str(z["model"]))
        out[m["id"]] = (m, pd.DataFrame(z["S"], columns=list(z["keys"])))
    return out


def two_sided(v, o):
    return float(min(1.0, 2 * min((v <= o).mean(), (v >= o).mean())))


def one_sided(v, o, d):
    if d == "lo":
        return float((v <= o).mean())
    return float((v >= o).mean())


def screen(models, obs):
    rows = []
    for mid, (m, S) in models.items():
        F = S[SCREEN].to_numpy(); o = np.array([obs[k] for k in SCREEN])
        mu = F.mean(0); Ci = np.linalg.pinv(np.cov(F.T))
        d2 = np.einsum("ij,jk,ik->i", F - mu, Ci, F - mu); do = float((o - mu) @ Ci @ (o - mu))
        r = {"model": mid, "persistence": m["pers"], "cycle_share": m["w"], "vol_shape": m["lam"],
             "maha_p": float((d2 >= do).mean())}
        for k in SCREEN + REPORT_ONLY:
            r[f"p_{k}"] = two_sided(S[k].to_numpy(), obs[k])
            r[f"sim_median_{k}"] = float(S[k].median())
        r["min_feature_p"] = min(r[f"p_{k}"] for k in SCREEN)
        r["plausible"] = bool(r["maha_p"] >= 0.05 and r["min_feature_p"] >= 0.01)
        rows.append(r)
    return pd.DataFrame(rows)


def calibrate(models, obs, plaus):
    stats = [k for k in DIRECTION]
    rows = []
    for mid, (m, S) in models.items():
        N = len(S)
        for k in stats:
            v = S[k].to_numpy(); o = obs[k]; p = one_sided(v, o, DIRECTION[k])
            rows.append({"model": mid, "plausible": mid in plaus, "stat": k, "direction": DIRECTION[k],
                         "observed": o, "null_mean": v.mean(), "null_sd": v.std(ddof=1),
                         "q025": np.quantile(v, .025), "q05": np.quantile(v, .05), "q50": np.quantile(v, .5),
                         "q95": np.quantile(v, .95), "q975": np.quantile(v, .975),
                         "p_one_sided": p, "mc_se": float(np.sqrt(max(p * (1 - p), 1 / N) / N)), "n_sims": N})
    return pd.DataFrame(rows)


def maxT(models, obs, plaus):
    """Selection-aware adjustment over the BATTERY: min of one-sided p-values,
    referred to its own null distribution (Westfall-Young min-p)."""
    rows = []
    for mid, (m, S) in models.items():
        P = np.column_stack([
            (S[k].rank(method="max") / len(S)).to_numpy() if DIRECTION[k] == "lo"
            else ((-S[k]).rank(method="max") / len(S)).to_numpy() for k in BATTERY])
        minp_null = P.min(1)
        p_obs = [one_sided(S[k].to_numpy(), obs[k], DIRECTION[k]) for k in BATTERY]
        mo = min(p_obs)
        rows.append({"model": mid, "plausible": mid in plaus, "min_raw_p": mo,
                     "which": BATTERY[int(np.argmin(p_obs))],
                     "adjusted_p": float((minp_null <= mo).mean()),
                     "crit_minp_5pct": float(np.quantile(minp_null, 0.05))})
    return pd.DataFrame(rows)


def breaks(models, obs, plaus):
    rows = []
    for mid, (m, S) in models.items():
        rows.append({"model": mid, "plausible": mid in plaus,
                     "share_K4": float((S.brk_K == 4).mean()),
                     "pct_max_adj": float((S.brk_maxadj < obs["brk_maxadj"]).mean()),
                     "pct_range": float((S.brk_range < obs["brk_range"]).mean()),
                     "p_max_adj": float((S.brk_maxadj >= obs["brk_maxadj"]).mean()),
                     "p_range": float((S.brk_range >= obs["brk_range"]).mean())})
    return pd.DataFrame(rows)


def summarize(cal: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for k, g in cal.groupby("stat", sort=False):
        P = g[g.plausible]; X = g[~g.plausible]
        d = DIRECTION[k]
        crit = P.q05.min() if d == "lo" else P.q95.max()     # least favourable over plausible models
        rows.append({"stat": k, "direction": d, "observed": g.observed.iloc[0],
                     "p_plausible_min": P.p_one_sided.min(), "p_plausible_median": P.p_one_sided.median(),
                     "p_plausible_max": P.p_one_sided.max(),
                     "p_extremes_min": X.p_one_sided.min(), "p_extremes_max": X.p_one_sided.max(),
                     "family_crit_5pct": crit,
                     "reject_at_family_crit": bool(g.observed.iloc[0] <= crit if d == "lo" else g.observed.iloc[0] >= crit),
                     "null_sd_plausible_range": f"{P.null_sd.min():.3f}-{P.null_sd.max():.3f}"})
    return pd.DataFrame(rows)


def main():
    obs = json.loads((ROOT / "outputs" / "reproduction.json").read_text())["battery_observed"]
    models = load("null_*.npz")
    scr = screen(models, obs)
    plaus = set(scr[scr.plausible].model)
    out = ROOT / "outputs"
    scr.to_csv(out / "screening.csv", index=False, float_format="%.4f")
    (out / "plausible_models.json").write_text(json.dumps(
        {"rule": "Mahalanobis p >= 0.05 on six residual features AND every feature p >= 0.01",
         "features": SCREEN, "plausible": sorted(plaus),
         "extremes": sorted(set(models) - plaus)}, indent=2) + "\n")
    cal = calibrate(models, obs, plaus)
    cal.to_csv(out / "calibration.csv", index=False, float_format="%.5f")
    summ = summarize(cal)
    summ.to_csv(out / "calibration_summary.csv", index=False, float_format="%.4f")
    mt = maxT(models, obs, plaus); mt.to_csv(out / "maxT.csv", index=False, float_format="%.4f")
    br = breaks(models, obs, plaus); br.to_csv(out / "breaks_null.csv", index=False, float_format="%.4f")
    pd.set_option("display.width", 220); pd.set_option("display.max_columns", 20)
    print(scr.sort_values("maha_p", ascending=False)[["model", "maha_p", "min_feature_p", "plausible"]].head(16).to_string(index=False))
    print(summ.to_string(index=False))
    print(mt.groupby("plausible")[["adjusted_p"]].describe().to_string())
    print(br.groupby("plausible")[["share_K4", "pct_max_adj", "pct_range"]].describe().round(3).to_string())


if __name__ == "__main__":
    main()
