#!/usr/bin/env python3
"""Residual unit-root diagnostics (v0.9).

ADF statistics at the v0.8 fixed lags, with residual-based critical values, and
the Phillips-Perron Z_t statistic computed with arch 8.0.0
(PhillipsPerron(trend="c"), Bartlett kernel) at 11 lags and at the automatic lag.

The v0.8 paper reported PP Z_t = -2.380. The scratch implementation behind that
number was not preserved and no standard specification reproduces it; v0.9
replaces it with the values computed here (-3.0416 at 11 lags, -3.3072 at the
automatic lag on the exact frozen file). The archived v0.8 value is still
recorded in the output, marked as unreconciled.

Critical values: Phillips-Ouliaris (1990) residual-based values, MacKinnon (2010)
response-surface values for two variables with a constant, and the ordinary
Dickey-Fuller constant-only value for reference. Critical values simulated for
the exact design (random walk around B ln t, with constant and with Bitcoin's
declining volatility) are produced by the v0.9 robustness package
(v09_robustness/scripts/11_unitroot_critical_values.py).
"""
from __future__ import annotations
import argparse, json, warnings
from pathlib import Path
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.adfvalues import mackinnoncrit
from reproduce_v08 import load_data, fit_powerlaw

warnings.filterwarnings('ignore', category=FutureWarning)
LAGS = [1, 5, 10, 21, 33]
PO_CRITICAL = {"1%": -3.96, "5%": -3.37, "10%": -3.07}       # Phillips-Ouliaris (1990), residual-based
DF_CONST_5PCT = -2.86                                          # ordinary DF, constant only (not appropriate for residuals)


def phillips_perron(r):
    import arch
    from arch.unitroot import PhillipsPerron
    lag11 = PhillipsPerron(r, lags=11, trend="c")
    auto = PhillipsPerron(r, trend="c")
    return {
        "implementation": f"arch {arch.__version__} PhillipsPerron(trend='c', test_type='tau'), Bartlett kernel",
        "Zt_lag11": float(lag11.stat),
        "Zt_auto": float(auto.stat),
        "auto_lags": int(auto.lags),
        "audited_v08_reported_Zt": -2.380,
        "v08_status": "not reproduced by any standard specification; replaced in v0.9",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv', type=Path)
    ap.add_argument('--allow-different-sample', action='store_true', help='skip v0.8 n/date-range enforcement')
    args = ap.parse_args()
    df = load_data(args.csv, require_frozen_shape=not args.allow_different_sample)
    fit = fit_powerlaw(df); r = fit.residuals
    mk = mackinnoncrit(N=2, regression='c', nobs=len(r))
    adf = {}
    for lag in LAGS:
        if len(r) <= lag + 5:
            continue
        stat = adfuller(r, maxlag=lag, regression='c', autolag=None)[0]
        adf[str(lag)] = {"statistic": float(stat), "reject_5pct_residual_based": bool(stat < PO_CRITICAL['5%'])}
    out = {
        "ADF": adf,
        "Phillips_Perron": phillips_perron(r),
        "critical_values": {
            "phillips_ouliaris_1990": PO_CRITICAL,
            "mackinnon_2010_N2_constant": {"1%": float(mk[0]), "5%": float(mk[1]), "10%": float(mk[2])},
            "dickey_fuller_constant_only_5pct_not_for_residuals": DF_CONST_5PCT,
        },
        "interpretation": ("Against residual-based 5% values, ADF rejects only at 21 and 33 lags and PP does not reject. "
                           "Against a random walk with Bitcoin's declining volatility (simulated in the v0.9 package), no statistic rejects."),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
