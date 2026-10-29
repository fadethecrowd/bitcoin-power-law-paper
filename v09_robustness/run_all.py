#!/usr/bin/env python3
"""Run the full v0.9 robustness study end to end.

    python run_all.py /path/to/btc_daily.csv [--allow-different-sample] [--workers 2]

About 20 minutes on two CPU cores (measured: 18 minutes). Every random draw is fixed by lib/config.py.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = ["01_reproduce.py", "02_simulate_nulls.py", "03_calibrate.py", "04_power.py",
         "05_hac_unitroot.py", "06_asymmetry.py", "08_bm_crosscheck.py", "09_sensitivity.py", "10_skew_battery.py", "11_unitroot_critical_values.py", "07_figures.py"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--allow-different-sample", action="store_true")
    ap.add_argument("--workers", default="2")
    a = ap.parse_args()
    for s in STEPS:
        cmd = [sys.executable, str(ROOT / "scripts" / s), a.csv]
        if a.allow_different_sample:
            cmd.append("--allow-different-sample")
        if s in {"02_simulate_nulls.py", "04_power.py", "05_hac_unitroot.py", "06_asymmetry.py", "09_sensitivity.py", "10_skew_battery.py", "11_unitroot_critical_values.py"}:
            cmd += ["--workers", a.workers]
        print(">>", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)
    subprocess.run([sys.executable, "-m", "pytest", "-q", str(ROOT / "tests")], check=False)


if __name__ == "__main__":
    main()
