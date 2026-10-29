#!/usr/bin/env python3
"""Step 10: does Bitcoin's right-skewed residual distribution change the exponent tests?

The declared family has Gaussian innovations, so simulated residuals are close to
symmetric (median skewness ~0) while the observed constant-B residuals are right
skewed (+0.86; +0.47 after standardizing by a rolling 4-year SD). Step 3 therefore
reports skewness but cannot screen on it.

This step re-runs the exponent battery for every plausible model with each null
path passed through the skew transform of step 6 (standardize by rolling 4-year
SD, rank-map onto the observed standardized residuals, restore the rolling SD,
rescale to the observed residual SD). Timing and persistence are kept; the
marginal distribution becomes Bitcoin's. One-sided p-values and the max-T
adjusted p-value are recomputed exactly as in step 3.

Writes outputs/skew_battery.csv.
"""
from __future__ import annotations

import argparse
import importlib.util
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
from lib.nulls import Generator, main_family, seed_for                 # noqa: E402
from lib.stats import Battery, BATTERY, DIRECTION                      # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


asym = _load("asym", "06_asymmetry.py")
cal = _load("cal", "03_calibrate.py")
_G = {}


def _init(csv, allow):
    asym._init(csv, allow)                                   # sets the observed standardized residuals
    df = load_data(Path(csv), require_frozen=not allow)
    D = design_from_df(df)
    _G.update(D=D, gen=asym._G["gen"], bat=Battery(D, make_detector(D.x[D.monthly])))


def run(args):
    k, m, n_paths = args
    D, gen, bat = _G["D"], _G["gen"], _G["bat"]
    rng = np.random.default_rng(seed_for("skew", k))
    rows = []
    for _ in range(n_paths):
        s, _v = bat.compute(C.B_FULL_V08 * D.x + asym.skewed(gen.draw(m, rng)))
        rows.append({kk: s[kk] for kk in list(DIRECTION) + ["skew"]})
    return m.id, pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--workers", type=int, default=2); ap.add_argument("--n", type=int, default=C.N_CALIBRATE)
    a = ap.parse_args()
    obs = json.loads((ROOT / "outputs" / "reproduction.json").read_text())["battery_observed"]
    plaus = json.loads((ROOT / "outputs" / "plausible_models.json").read_text())["plausible"]
    fam = main_family()
    jobs = [(k, m, a.n) for k, m in enumerate(fam) if m.id in plaus]
    t0 = time.time(); models = {}
    with Pool(a.workers, initializer=_init, initargs=(a.csv, a.allow_different_sample)) as pool:
        for mid, S in pool.imap_unordered(run, jobs):
            models[mid] = (None, S); print(f"{mid:28s} {time.time()-t0:6.0f}s", flush=True)
    C_ = cal.calibrate(models, obs, set(plaus))
    mt = cal.maxT(models, obs, set(plaus)).set_index("model")
    piv = C_.pivot(index="model", columns="stat", values="p_one_sided")[BATTERY + ["rsd5", "exp_range"]]
    sk = pd.Series({mid: float(S["skew"].median()) for mid, (_, S) in models.items()}, name="median_sim_skew")
    T = piv.join(mt[["adjusted_p", "which"]]).join(sk)
    base = pd.read_csv(ROOT / "outputs" / "maxT.csv").set_index("model")["adjusted_p"].rename("adjusted_p_gaussian")
    T = T.join(base)
    T.to_csv(ROOT / "outputs" / "skew_battery.csv", float_format="%.4f")
    pd.set_option("display.width", 220)
    print(T.round(3).to_string())


if __name__ == "__main__":
    main()
