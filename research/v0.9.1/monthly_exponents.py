#!/usr/bin/env python3
"""v0.9.1 descriptive monthly exponent audit. Not a structural-break test.

Usage: python research/v0.9.1/monthly_exponents.py PRIVATE_CSV --out monthly_summary.csv
Input columns: date, price_usd, days_since_genesis.
Do not commit input CSV, daily prices, or daily residuals to GitHub.
"""
import argparse
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

GENESIS = pd.Timestamp("2009-01-03")
EXPECTED_FROZEN_SHA256 = "ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f"

def fit(x, y):
    return float(np.polyfit(x, y, 1)[0])

def audit(path):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    df = pd.read_csv(path, parse_dates=["date"]).sort_values("date")
    if not {"date", "price_usd", "days_since_genesis"}.issubset(df):
        raise ValueError("Missing mandatory columns")
    if df.date.duplicated().any() or not df.date.diff().dropna().eq(pd.Timedelta(days=1)).all():
        raise ValueError("Dates not complete, consecutive, and unique")
    if not (df.price_usd > 0).all():
        raise ValueError("Prices must be strictly positive")
    expected_days = (df.date - GENESIS).dt.days
    if not np.array_equal(expected_days.to_numpy(), df.days_since_genesis.to_numpy()):
        raise ValueError("days_since_genesis mismatch")
    x = np.log(df.days_since_genesis.to_numpy(float))
    y = np.log(df.price_usd.to_numpy(float))
    rows = []
    for period in df.date.dt.to_period("M").unique():
        end = df.loc[df.date.dt.to_period("M").eq(period), "date"].iloc[-1]
        end_idx = int(df.date.searchsorted(end, side="right"))
        if end_idx < 365:
            continue
        item = {"month": str(period), "end": end.date().isoformat(), "expanding_B": fit(x[:end_idx], y[:end_idx])}
        for years in (3, 5, 7, 10):
            start = end - pd.Timedelta(days=365.25 * years)
            start_idx = int(df.date.searchsorted(start, side="right"))
            days = end_idx - start_idx
            item[f"rolling_{years}y_B"] = fit(x[start_idx:end_idx], y[start_idx:end_idx]) if days >= years * 360 else float("nan")
        rows.append(item)
    return digest, pd.DataFrame(rows), fit(x, y)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--out", default="monthly_summary.csv")
    parser.add_argument("--require-frozen-hash", action="store_true")
    args = parser.parse_args()
    digest, summary, full = audit(args.csv)
    if args.require_frozen_hash and digest != EXPECTED_FROZEN_SHA256:
        raise SystemExit("SHA-256 does not match original frozen research series")
    summary.to_csv(args.out, index=False)
    print(f"SHA256={digest} rows={len(pd.read_csv(args.csv))} full_B={full:.10f}")
    print(summary.tail(12).to_string(index=False))
    print("DESCRIPTIVE ONLY. These estimates have not been tested against constant-B null envelopes.")

if __name__ == "__main__":
    main()
