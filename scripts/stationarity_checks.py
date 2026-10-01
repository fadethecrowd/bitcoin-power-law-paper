#!/usr/bin/env python3
"""Residual unit-root diagnostics described in v0.8.

This publication reconstruction reproduces the ADF / residual-critical-value
checks that can be specified from the surviving audit record. The original
Phillips-Perron scratch implementation was not preserved, and the v0.8 PP
statistic could not be reproduced unambiguously with a standard public
implementation. To avoid publishing a contradictory result as if it were an
exact reconstruction, PP is documented but not recomputed here.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from statsmodels.tsa.stattools import adfuller
from reproduce_v08 import load_data, fit_powerlaw

LAGS=[1,5,10,21,33]
EG_CRITICAL={"1%":-3.96,"5%":-3.37,"10%":-3.07}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('csv',type=Path)
    ap.add_argument('--allow-different-sample',action='store_true',help='skip v0.8 n/date-range enforcement')
    args=ap.parse_args()
    df=load_data(args.csv,require_frozen_shape=not args.allow_different_sample)
    fit=fit_powerlaw(df);r=fit.residuals
    adf={}
    for lag in LAGS:
        if len(r) <= lag + 5:
            continue
        stat=adfuller(r,maxlag=lag,regression='c',autolag=None)[0]
        adf[str(lag)]={"statistic":float(stat),"eg_style_reject_5pct":bool(stat < EG_CRITICAL['5%'])}
    pp={
        "audited_v08_reported_Zt":-2.380,
        "reported_newey_west_lag":11,
        "status":"not recomputed in the public reconstruction",
        "reason":"The original PP implementation was not preserved, and standard reconstructed implementations did not reproduce the reported v0.8 statistic. The discrepancy is unresolved and is reserved for a later paper revision/re-audit."
    }
    out={
        "ADF":adf,
        "engle_granger_style_residual_critical_values":EG_CRITICAL,
        "Phillips_Perron":pp,
        "interpretation":"ADF/residual evidence is lag-dependent. The v0.8 Phillips-Perron value is retained as an audited reported value but is not independently reproduced by this public code."
    }
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
