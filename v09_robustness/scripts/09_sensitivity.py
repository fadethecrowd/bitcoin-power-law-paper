#!/usr/bin/env python3
"""Step 9: sensitivity of the calibration to the declared family's fixed choices.

For every plausible model, four variants are simulated: volatility shape
lam = 0.5 and 1.25 (Baquero & Menezes allow up to 1.25), and cycle periods of
3.5 and 4.5 years. Each variant is screened with the same rule and the battery
is recalibrated.

Writes outputs/sensitivity.csv.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
import importlib.util                                                        # noqa: E402
spec = importlib.util.spec_from_file_location("cal", ROOT / "scripts" / "03_calibrate.py")
cal = importlib.util.module_from_spec(spec); spec.loader.exec_module(cal)     # noqa: E402
from lib.stats import BATTERY                                                # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--workers", default="2")
    a = ap.parse_args()
    cmd = [sys.executable, str(ROOT / "scripts" / "02_simulate_nulls.py"), a.csv, "--sensitivity", "--workers", a.workers]
    if a.allow_different_sample:
        cmd.append("--allow-different-sample")
    subprocess.run(cmd, check=True)
    obs = json.loads((ROOT / "outputs" / "reproduction.json").read_text())["battery_observed"]
    models = cal.load("sens_*.npz")
    scr = cal.screen(models, obs).set_index("model")
    C_ = cal.calibrate(models, obs, set(scr.index[scr.plausible]))
    mt = cal.maxT(models, obs, set(scr.index[scr.plausible])).set_index("model")
    piv = C_.pivot(index="model", columns="stat", values="p_one_sided")[BATTERY + ["rsd5", "exp_range"]]
    T = scr[["maha_p", "min_feature_p", "plausible"]].join(piv).join(mt[["adjusted_p"]])
    T.to_csv(ROOT / "outputs" / "sensitivity.csv", float_format="%.4f")
    pd.set_option("display.width", 220)
    print(T.round(3).to_string())
    print(T.groupby("plausible")[BATTERY + ["adjusted_p"]].agg(["min", "median", "max"]).round(3).T.to_string())


if __name__ == "__main__":
    main()
