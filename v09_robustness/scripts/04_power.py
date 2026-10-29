#!/usr/bin/env python3
"""Step 4: power of each statistic against declining local exponents.

Alternative histories:  ln P_t = B ln t + g_{shape,D}(ln t) + u_t,  where g is
defined in lib/nulls.trend_deviation and u_t is drawn from a plausible null
model. For every noise model, N_POWER noise paths are drawn once and reused
for every D (common random numbers), with seeds independent of the calibration
draws, so the D = 0 row is an honest out-of-sample false-positive rate.

Critical values:
  family : least favourable 5% critical value over all plausible models
           (controls size across the declared plausible family)
  model  : the 5% critical value of the same model that generated the noise
           (an oracle benchmark: the noise model is known)
The max-T battery test uses model-specific calibration only.

Writes outputs/power_curves.csv and outputs/size_table.csv.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                           # noqa: E402
from lib.core import load_data, design_from_df, make_detector         # noqa: E402
from lib.nulls import Generator, Model, seed_for, trend_deviation      # noqa: E402
from lib.stats import Battery, DIRECTION, BATTERY                      # noqa: E402

TESTS = ["curv", "d17", "mean5", "r5_2025", "rend5", "rmin5", "rend4", "rend6", "rend8", "rend10",
         "rmin4", "rmin6", "rmin8", "rmin10", "exp_drop", "brk_maxadj", "brk_range"]
_G = {}


def _init(csv, allow):
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df); y = np.log(df.price_usd.to_numpy(float))
    X1 = np.column_stack([np.ones(D.n), D.xc]); resid_sd = float(np.std(y - X1 @ (D.P1 @ y), ddof=1))
    x_late = float(D.x[D.i_post])
    _G.update(D=D, gen=Generator(df, resid_sd, D.x), bat=Battery(D, make_detector(D.x[D.monthly])),
              g={(s, d): trend_deviation(D.x, s, d, x_late) for s in C.SHAPES for d in C.DELTAS})


def run(args):
    k, m, n_paths = args
    D, gen, bat, g = _G["D"], _G["gen"], _G["bat"], _G["g"]
    rng = np.random.default_rng(seed_for("power", k))
    rows = []
    for i in range(n_paths):
        u = gen.draw(m, rng)
        base = C.B_FULL_V08 * D.x + u
        for (s, d), gd in g.items():
            st, _ = bat.compute(base + gd, with_features=False)
            st.update(shape=s, delta=d, path=i)
            rows.append(st)
    return m.id, pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--n", type=int, default=C.N_POWER); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    out = ROOT / "outputs"
    plaus = json.loads((out / "plausible_models.json").read_text())["plausible"]
    cal = pd.read_csv(out / "calibration.csv")
    # null samples for the max-T calibration (model-specific)
    nulls = {}
    for f in glob.glob(str(ROOT / "cache" / "null_*.npz")):
        z = np.load(f); mid = json.loads(str(z["model"]))["id"]
        if mid in plaus:
            nulls[mid] = pd.DataFrame(z["S"], columns=list(z["keys"]))
    fam = {}
    for k in TESTS:
        g = cal[(cal.stat == k) & cal.plausible]
        fam[k] = g.q05.min() if DIRECTION[k] == "lo" else g.q95.max()
    models = []
    for f in sorted(glob.glob(str(ROOT / "cache" / "null_*.npz"))):
        md = json.loads(str(np.load(f)["model"]))
        if md["id"] in plaus:
            models.append(Model(md["pers"], md["kind"], md["par"], md["w"], md["lam"], md["period"]))
    jobs = [(i, m, a.n) for i, m in enumerate(models)]
    t0 = time.time(); res = {}
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for mid, df_ in pool.imap_unordered(run, jobs):
            res[mid] = df_; print(f"{mid:28s} {time.time()-t0:6.0f}s", flush=True)
    rows = []
    for mid, R in res.items():
        Nul = nulls[mid]
        mcrit = {k: (cal[(cal.model == mid) & (cal.stat == k)].q05.iloc[0] if DIRECTION[k] == "lo"
                     else cal[(cal.model == mid) & (cal.stat == k)].q95.iloc[0]) for k in TESTS}
        # max-T: one-sided p of each battery stat relative to this model's null sample
        nullP = np.column_stack([(Nul[k].rank(method="max") / len(Nul)).to_numpy() if DIRECTION[k] == "lo"
                                 else ((-Nul[k]).rank(method="max") / len(Nul)).to_numpy() for k in BATTERY])
        crit_minp = np.quantile(nullP.min(1), 0.05)
        sorted_null = {k: np.sort(Nul[k].to_numpy()) for k in BATTERY}
        def pcol(k, v):
            s = sorted_null[k]
            return (np.searchsorted(s, v, side="right") / len(s)) if DIRECTION[k] == "lo" \
                else (1 - np.searchsorted(s, v, side="left") / len(s))
        for (s, d), G in R.groupby(["shape", "delta"]):
            N = len(G)
            for k in TESTS:
                v = G[k].to_numpy()
                rf = (v <= fam[k]).mean() if DIRECTION[k] == "lo" else (v >= fam[k]).mean()
                rm = (v <= mcrit[k]).mean() if DIRECTION[k] == "lo" else (v >= mcrit[k]).mean()
                rows.append({"model": mid, "shape": s, "delta": d, "test": k, "reject_family": rf,
                             "reject_model": rm, "mc_se_family": np.sqrt(max(rf * (1 - rf), 1 / N) / N), "n": N,
                             "mean_stat": v.mean()})
            minp = np.column_stack([pcol(k, G[k].to_numpy()) for k in BATTERY]).min(1)
            r = (minp <= crit_minp).mean()
            rows.append({"model": mid, "shape": s, "delta": d, "test": "maxT_battery", "reject_family": np.nan,
                         "reject_model": r, "mc_se_family": np.sqrt(max(r * (1 - r), 1 / N) / N), "n": N,
                         "mean_stat": np.nan})
    order = {m.id: i for i, m in enumerate(models)}            # job order, not completion order
    P = pd.DataFrame(rows)
    P = P.sort_values("model", key=lambda s: s.map(order), kind="mergesort").reset_index(drop=True)
    P.to_csv(out / "power_curves.csv", index=False, float_format="%.4f")
    size = P[P.delta == 0].pivot_table(index="test", values=["reject_family", "reject_model"],
                                       aggfunc=["min", "max", "mean"])
    size.to_csv(out / "size_table.csv", float_format="%.4f")
    summ = P.groupby(["shape", "test", "delta"]).agg(fam_mean=("reject_family", "mean"), fam_min=("reject_family", "min"),
                                                     fam_max=("reject_family", "max"), mod_mean=("reject_model", "mean"))
    pd.set_option("display.width", 200); pd.set_option("display.max_rows", 400)
    print(summ.unstack("delta")["fam_mean"].round(3).to_string())
    print(summ.unstack("delta")["mod_mean"].round(3).to_string())
    print(size.round(3).to_string())
    print(f"total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
