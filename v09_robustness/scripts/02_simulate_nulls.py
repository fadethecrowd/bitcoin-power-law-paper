#!/usr/bin/env python3
"""Step 2: simulate every member of the declared null family (constant B).

For each model, N_CALIBRATE histories ln P = B ln t + u are drawn and the full
test battery, the break detector and the screening features are computed.
Per-path statistics of *simulated* histories are cached in cache/ (they
contain no real price data); null bands for figures are reduced to quantiles.

Usage: python scripts/02_simulate_nulls.py DATA.csv [--models all|plausible] [--workers 2]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import config as C                                           # noqa: E402
from lib.core import load_data, design_from_df, make_detector         # noqa: E402
from lib.nulls import Generator, Model, main_family, seed_for          # noqa: E402
from lib.stats import Battery                                          # noqa: E402

CACHE = ROOT / "cache"
_G = {}


def _init(csv, allow):
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df)
    y = np.log(df.price_usd.to_numpy(float))
    X1 = np.column_stack([np.ones(D.n), D.xc])
    resid_sd = float(np.std(y - X1 @ (D.P1 @ y), ddof=1))     # observed residual SD, 0.69709
    _G.update(D=D, gen=Generator(df, resid_sd, D.x),
              bat=Battery(D, make_detector(D.x[D.monthly])))


def run_model(args):
    k, m, n_paths, stage, tag = args
    D, gen, bat = _G["D"], _G["gen"], _G["bat"]
    rng = np.random.default_rng(seed_for(stage, k))
    rows, vecs = [], {}
    t0 = time.time()
    for _ in range(n_paths):
        u = gen.draw(m, rng)
        s, v = bat.compute(C.B_FULL_V08 * D.x + u)
        rows.append(s)
        for key, arr in v.items():
            vecs.setdefault(key, []).append(arr)
    keys = list(rows[0].keys())
    S = np.array([[r[k_] for k_ in keys] for r in rows], dtype=float)
    bands = {}
    for key, lst in vecs.items():
        A = np.vstack(lst)
        bands[key] = np.quantile(A, [0.025, 0.05, 0.5, 0.95, 0.975], axis=0)
    np.savez_compressed(CACHE / f"{tag}_{k:03d}.npz", S=S, keys=np.array(keys),
                        model=json.dumps(m.as_dict()), **{f"band_{b}": q for b, q in bands.items()})
    return m.id, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--n", type=int, default=C.N_CALIBRATE)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--only", type=str, default="", help="comma-separated model indices (debug)")
    ap.add_argument("--sensitivity", action="store_true",
                    help="simulate the sensitivity variants of the models listed in outputs/plausible_models.json")
    a = ap.parse_args()
    CACHE.mkdir(exist_ok=True)
    if a.sensitivity:
        base = json.loads((ROOT / "outputs" / "plausible_models.json").read_text())["plausible"]
        jobs = []
        k = 0
        for mid in base:
            m0 = next(m for m in main_family() if m.id == mid)
            for var in C.SENSITIVITY_VARIANTS:
                kw = {f: getattr(m0, f) for f in ["pers", "kind", "par", "w", "lam", "period"]}
                kw.update({kk: vv for kk, vv in var.items() if kk != "tag"})
                if kw == {f: getattr(m0, f) for f in ["pers", "kind", "par", "w", "lam", "period"]}:
                    continue
                jobs.append((k, Model(**kw), a.n, "sens", "sens")); k += 1
        # A volatility variant of a lam0/lam1 pair is the same model twice (e.g. lam1.25 of
        # both). Keep one copy per model id: the last, so seeds match the published run.
        last = {m.id: kk for kk, m, *_ in jobs}
        jobs = [j for j in jobs if last[j[1].id] == j[0]]
    else:
        fam = main_family()
        idx = [int(i) for i in a.only.split(",")] if a.only else range(len(fam))
        jobs = [(k, fam[k], a.n, "calibrate", "null") for k in idx]
    t0 = time.time()
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for mid, dt in pool.imap_unordered(run_model, jobs):
            print(f"{mid:32s} {dt:6.1f}s", flush=True)
    print(f"done {len(jobs)} models in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
