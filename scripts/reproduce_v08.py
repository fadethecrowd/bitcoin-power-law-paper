#!/usr/bin/env python3
"""Deterministic v0.8 reproduction calculations from a user-supplied BTC daily-close CSV.

This is a publication reconstruction from the frozen methods/audit record. It is
not an archival copy of the original August 2026 scratch scripts, which were not
preserved. It intentionally emits aggregate statistics only.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr
from statsmodels.stats.sandwich_covariance import cov_hac

GENESIS = pd.Timestamp("2009-01-03")
FROZEN_FIRST = pd.Timestamp("2010-07-17")
FROZEN_LAST = pd.Timestamp("2026-08-14")
FROZEN_N = 5873
YEAR_DAYS = 365.25


def load_data(path: Path, require_frozen_shape: bool = True) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"date", "timestamp", "price_usd", "days_since_genesis"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df = df.sort_values("date").reset_index(drop=True)
    if (df["price_usd"] <= 0).any():
        raise ValueError("price_usd must be positive")
    if df["date"].duplicated().any():
        raise ValueError("duplicate dates")
    if len(df) > 1:
        gaps = df["date"].diff().iloc[1:] != pd.Timedelta(days=1)
        if gaps.any():
            raise ValueError(f"date gaps detected: {int(gaps.sum())}")
    expected_days = (df["date"] - GENESIS).dt.days.to_numpy()
    if not np.array_equal(expected_days, df["days_since_genesis"].to_numpy()):
        raise ValueError("days_since_genesis does not match 2009-01-03 genesis convention")
    if require_frozen_shape:
        if len(df) != FROZEN_N or df.iloc[0].date != FROZEN_FIRST or df.iloc[-1].date != FROZEN_LAST:
            raise ValueError(
                "input does not have the frozen v0.8 sample shape: "
                f"expected n={FROZEN_N}, {FROZEN_FIRST.date()}..{FROZEN_LAST.date()}"
            )
    return df


@dataclass
class Fit:
    intercept: float
    A: float
    B: float
    r2: float
    residual_sd_sample: float
    naive_se_B: float
    residuals: np.ndarray


def fit_powerlaw(df: pd.DataFrame) -> Fit:
    x = np.log(df["days_since_genesis"].to_numpy(float))
    y = np.log(df["price_usd"].to_numpy(float))
    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit()
    residuals = np.asarray(res.resid)
    return Fit(
        intercept=float(res.params[0]),
        A=float(math.exp(res.params[0])),
        B=float(res.params[1]),
        r2=float(res.rsquared),
        residual_sd_sample=float(np.std(residuals, ddof=1)),
        naive_se_B=float(res.bse[1]),
        residuals=residuals,
    )


def hac_se_B(df: pd.DataFrame, nlags: int = 365) -> float:
    x = np.log(df["days_since_genesis"].to_numpy(float))
    y = np.log(df["price_usd"].to_numpy(float))
    res = sm.OLS(y, sm.add_constant(x)).fit()
    # Original audited value 0.18916 is reproduced with no small-sample correction.
    cov = cov_hac(res, nlags=nlags, use_correction=False)
    return float(math.sqrt(cov[1, 1]))


def sampling_robustness(df: pd.DataFrame) -> dict:
    indexed = df.set_index("date")
    weekly = indexed.resample("W-SUN").last().dropna().reset_index()
    monthly = indexed.resample("ME").last().dropna().reset_index()
    return {
        "daily_B": fit_powerlaw(df).B,
        "weekly_B": fit_powerlaw(weekly).B,
        "monthly_B": fit_powerlaw(monthly).B,
    }


def expanding_B(df: pd.DataFrame) -> dict:
    dates = [
        "2016-12-31", "2018-12-31", "2020-12-31", "2021-12-31",
        "2022-12-31", "2023-12-31", "2024-12-31", "2025-12-31", "2026-08-14",
    ]
    out = {}
    first=df.iloc[0].date; last=df.iloc[-1].date
    for d in dates:
        cutoff=pd.Timestamp(d)
        if cutoff < first or cutoff > last:
            continue
        sub = df[df.date <= cutoff]
        if len(sub) < 30:
            continue
        f = fit_powerlaw(sub)
        out[d] = {"n": len(sub), "B": f.B, "hac365_se_B": hac_se_B(sub, min(365,len(sub)-2))}
    return out


def strict_episodes(df: pd.DataFrame, residuals: np.ndarray, min_days: int = 60) -> list[tuple[int, int]]:
    neg = residuals < 0
    out: list[tuple[int, int]] = []
    i = 0
    while i < len(df):
        if not neg[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(df) and neg[j + 1]:
            j += 1
        if j - i + 1 >= min_days:
            out.append((i, j))
        i = j + 1
    return out


def trailing_four_year_stats(df: pd.DataFrame, residuals: np.ndarray, idx: int):
    date = df.loc[idx, "date"]
    start = date - pd.DateOffset(years=4)
    mask = (df["date"] >= start) & (df["date"] < date)
    w = residuals[mask.to_numpy()]
    if len(w) < 1400:
        return None
    mean = float(np.mean(w))
    sd = float(np.std(w, ddof=0))
    rms = float(math.sqrt(np.mean(w * w)))
    return mean, sd, rms


def episode_analysis(df: pd.DataFrame, fit: Fit) -> dict:
    r = fit.residuals
    eps = strict_episodes(df, r)
    rows = []
    for number, (i, j) in enumerate(eps, 1):
        seg = r[i:j+1]
        min_i = i + int(np.argmin(seg))
        local_values = []
        for k in range(i, j + 1):
            stats = trailing_four_year_stats(df, r, k)
            if stats is None:
                continue
            mean, sd, rms = stats
            local_values.append((k, r[k]/sd, (r[k]-mean)/sd, r[k]/rms))
        rec = {
            "number": number,
            "start": str(df.loc[i, "date"].date()),
            "end": str(df.loc[j, "date"].date()),
            "open": bool(j == len(df)-1),
            "duration_days": int(j-i+1),
            "mean_raw_residual": float(np.mean(seg)),
            "minimum_raw_residual": float(np.min(seg)),
            "minimum_raw_date": str(df.loc[min_i, "date"].date()),
            "cumulative_negative_area_log_days": float(-np.sum(seg)),
        }
        if local_values:
            vals = np.array([[x[1],x[2],x[3]] for x in local_values])
            rec.update({
                "minimum_local_sigma_depth": float(np.min(vals[:,0])),
                "mean_local_sigma_depth": float(np.mean(vals[:,0])),
                "minimum_local_demeaned_z": float(np.min(vals[:,1])),
                "mean_local_demeaned_z": float(np.mean(vals[:,1])),
                "minimum_rms_depth": float(np.min(vals[:,2])),
                "mean_rms_depth": float(np.mean(vals[:,2])),
            })
        rows.append(rec)
    current = rows[-1]
    current_idx = len(df)-1
    mean, sd, rms = trailing_four_year_stats(df, r, current_idx)
    cur = {
        "date": str(df.iloc[-1].date.date()),
        "price_usd": float(df.iloc[-1].price_usd),
        "trend_usd": float(math.exp(fit.intercept + fit.B*math.log(float(df.iloc[-1].days_since_genesis)))),
        "raw_residual": float(r[-1]),
        "trailing_4y_mean": mean,
        "trailing_4y_sd_population": sd,
        "trailing_4y_rms_about_zero": rms,
        "local_sigma_depth": float(r[-1]/sd),
        "local_demeaned_z": float((r[-1]-mean)/sd),
        "rms_depth": float(r[-1]/rms),
    }
    return {"episodes": rows, "current": cur}


def residual_slope_per_year(df: pd.DataFrame, r: np.ndarray, start_idx: int, end_idx: int) -> float:
    t = (df.loc[start_idx:end_idx, "date"] - df.loc[start_idx, "date"]).dt.days.to_numpy(float) / YEAR_DAYS
    y = r[start_idx:end_idx+1]
    if len(y) < 2:
        return float("nan")
    return float(np.polyfit(t, y, 1)[0])


def current_path_stats(df: pd.DataFrame, fit: Fit, episode_start_idx: int) -> dict:
    r = fit.residuals
    i = episode_start_idx
    j = len(df)-1
    min_i = i + int(np.argmin(r[i:j+1]))
    third_groups = np.array_split(np.arange(i, j+1), 3)
    out = {
        "minimum_date": str(df.loc[min_i,"date"].date()),
        "minimum_raw_residual": float(r[min_i]),
        "elapsed_days_min_to_cutoff": int((df.loc[j,"date"]-df.loc[min_i,"date"]).days),
        "observations_min_to_cutoff_inclusive": int(j-min_i+1),
        "price_change_since_min": float(df.loc[j,"price_usd"]/df.loc[min_i,"price_usd"]-1),
        "residual_change_since_min": float(r[j]-r[min_i]),
        "thirds_mean_residual": [float(np.mean(r[g])) for g in third_groups],
        "post_min_slope_log_per_year": residual_slope_per_year(df,r,min_i,j),
    }
    for horizon in (90,180,365):
        start=max(0,j-horizon+1)
        out[f"slope_{horizon}d_log_per_year"] = residual_slope_per_year(df,r,start,j)
    out["episode_slope_log_per_year"] = residual_slope_per_year(df,r,i,j)
    return out


def refit_analysis(df: pd.DataFrame, full_fit: Fit, episode_start_idx: int) -> dict:
    # Freeze using information strictly before the first below-trend day.
    frozen = fit_powerlaw(df.iloc[:episode_start_idx])
    t = float(df.iloc[-1].days_since_genesis)
    price = float(df.iloc[-1].price_usd)
    frozen_trend = math.exp(frozen.intercept + frozen.B*math.log(t))
    refit_trend = math.exp(full_fit.intercept + full_fit.B*math.log(t))
    frozen_log_deficit = math.log(frozen_trend/price)
    refit_log_deficit = math.log(refit_trend/price)
    frozen_price_gap = frozen_trend-price
    refit_price_gap = refit_trend-price
    return {
        "episode_start_B": frozen.B,
        "current_B": full_fit.B,
        "delta_B": full_fit.B-frozen.B,
        "episode_start_frozen_trend_at_cutoff_usd": frozen_trend,
        "current_refit_trend_at_cutoff_usd": refit_trend,
        "trend_reduction_fraction": 1-refit_trend/frozen_trend,
        "refit_absorption_log_fraction": 1-refit_log_deficit/frozen_log_deficit,
        "refit_absorption_price_fraction": 1-refit_price_gap/frozen_price_gap,
        "absorbed_price_gap_usd": frozen_price_gap-refit_price_gap,
        "original_frozen_price_gap_usd": frozen_price_gap,
    }


def rolling_ar1(values: np.ndarray, window: int) -> tuple[np.ndarray,np.ndarray]:
    rhos=[]; sds=[]
    for end in range(window, len(values)+1):
        w=values[end-window:end]
        x=w[:-1]; y=w[1:]
        X=np.column_stack([np.ones(len(x)),x])
        beta=np.linalg.lstsq(X,y,rcond=None)[0]
        rhos.append(beta[1]); sds.append(np.std(w,ddof=0))
    return np.asarray(rhos),np.asarray(sds)


def persistence_summary(df: pd.DataFrame, residuals: np.ndarray) -> dict:
    out={}
    for years,window in [(2,730),(4,1461),(6,2191)]:
        rho,sd=rolling_ar1(residuals,window)
        valid=(rho>0)&(rho<1)
        half=np.full_like(rho,np.nan,dtype=float)
        half[valid]=math.log(2)/(-np.log(rho[valid]))
        out[f"{years}y"]={
            "n_windows":int(len(rho)),
            "rho_min":float(np.min(rho)),"rho_max":float(np.max(rho)),"rho_median":float(np.median(rho)),
            "half_life_median_days_stationary_only":float(np.nanmedian(half)),
            "pearson_sd_rho":float(np.corrcoef(sd,rho)[0,1]),
            "spearman_sd_rho":float(spearmanr(sd,rho).statistic),
        }
    return out


def recovery_clock(df: pd.DataFrame, residuals: np.ndarray, episodes: list[tuple[int,int]]) -> dict:
    logp=np.log(df["price_usd"].to_numpy(float))
    returns=np.r_[np.nan,np.diff(logp)]
    days=[]; vtime=[]
    for i,j in episodes:
        m=i+int(np.argmin(residuals[i:j+1]))
        days.append(j-m+1)
        # Accumulated movement after the trough through the last negative day.
        vtime.append(float(np.nansum(np.abs(returns[m+1:j+1]))))
    days=np.asarray(days,float);vtime=np.asarray(vtime,float)
    return {
        "n_completed_episodes":int(len(days)),
        "calendar_time_cv_population":float(np.std(days,ddof=0)/np.mean(days)),
        "volatility_time_cv_population":float(np.std(vtime,ddof=0)/np.mean(vtime)),
    }


def trend_and_return_context(df: pd.DataFrame, fit: Fit) -> dict:
    last=df.iloc[-1]
    t=float(last.days_since_genesis); price=float(last.price_usd)
    horizons=[1,2,3,4,5,10]
    keep={}; catch={}
    for h in horizons:
        future_t=t+YEAR_DAYS*h
        gross=(future_t/t)**fit.B
        keep[str(h)] = gross**(1/h)-1
        future_trend=fit.A*future_t**fit.B
        catch[str(h)] = (future_trend/price)**(1/h)-1
    # Historical calendar-year CAGRs. Era labels are by start date, matching v0.8.
    date_to_idx={d:i for i,d in enumerate(df.date)}
    def windows(h, start_min=None):
        vals=[]
        for i,row in df.iterrows():
            if start_min is not None and row.date < pd.Timestamp(start_min):
                continue
            end=row.date+pd.DateOffset(years=h)
            j=date_to_idx.get(end)
            if j is None: continue
            vals.append((i,j,(float(df.loc[j,"price_usd"])/float(row.price_usd))**(1/h)-1))
        return vals
    k1=keep["1"]
    keep_occ={}
    for name,start in [("all",None),("post_2016","2016-01-01"),("post_2020","2020-01-01")]:
        w=windows(1,start)
        keep_occ[name]=float(np.mean([v>=k1 for _,_,v in w]))
    catch_occ={}
    independent_equiv={}
    for h in [1,2,3,4,5]:
        w=windows(h,"2020-01-01")
        catch_occ[str(h)] = float(np.mean([v>=catch[str(h)] for _,_,v in w])) if w else None
        if w:
            span_days=(df.loc[w[-1][0],"date"]-df.loc[w[0][0],"date"]).days
            independent_equiv[str(h)]=float(span_days/(YEAR_DAYS*h))
    contemporaneous={}
    for h in [1,2,3]:
        w=windows(h,"2020-01-01")
        realized=[]; hurdle=[]; beat=[]
        for i,j,cagr in w:
            t0=float(df.loc[i,"days_since_genesis"]);t1=float(df.loc[j,"days_since_genesis"])
            h0=((t1/t0)**fit.B)**(1/h)-1
            realized.append(cagr);hurdle.append(h0);beat.append(cagr>=h0)
        contemporaneous[str(h)]={
            "median_realized_cagr":float(np.median(realized)) if realized else None,
            "median_frozen_fit_hurdle_at_window_start":float(np.median(hurdle)) if hurdle else None,
            "share_beating_hurdle":float(np.mean(beat)) if beat else None,
        }
    return {
        "annualized_instantaneous_log_growth":fit.B/t*YEAR_DAYS,
        "instantaneous_arithmetic_equivalent":math.exp(fit.B/t*YEAR_DAYS)-1,
        "keep_pace_cagr":keep,
        "catch_up_cagr":catch,
        "keep_pace_1y_occupancy":keep_occ,
        "post_2020_catch_up_occupancy":catch_occ,
        "post_2020_independent_window_equivalents":independent_equiv,
        "post_2020_realized_vs_frozen_fit_start_hurdle":contemporaneous,
    }



def trend_volatility_context(df: pd.DataFrame, fit: Fit) -> dict:
    ret=np.log(df["price_usd"].to_numpy(float))
    ret=np.r_[np.nan,np.diff(ret)]
    preferred=["2012-12-31","2016-12-31","2020-12-31","2024-12-31","2026-08-14"]
    rows={}
    for d in preferred:
        hits=df.index[df.date==pd.Timestamp(d)]
        if len(hits)==0:
            continue
        idx=int(hits[0])
        # Research convention: 730 daily log returns ending at the checkpoint,
        # population SD, annualized by sqrt(365).
        if idx < 730:
            continue
        w=ret[idx-730+1:idx+1]
        vol=float(np.nanstd(w,ddof=0)*math.sqrt(365.0))
        t=float(df.loc[idx,"days_since_genesis"])
        log_hurdle=float(fit.B/t*YEAR_DAYS)
        rows[d]={"annualized_return_volatility_sd":vol,"annualized_trend_log_growth":log_hurdle,"movement_scale_ratio":vol/log_hurdle}
    out={"checkpoints":rows,"return_volatility_convention":"730 daily log returns; population SD; annualized by sqrt(365)"}
    if len(rows)>=2:
        keys=list(rows)
        first=rows[keys[0]];last=rows[keys[-1]]
        out["trend_log_growth_decline_fraction"]=1-last["annualized_trend_log_growth"]/first["annualized_trend_log_growth"]
        out["return_volatility_decline_fraction"]=1-last["annualized_return_volatility_sd"]/first["annualized_return_volatility_sd"]
    else:
        out["trend_log_growth_decline_fraction"]=None
        out["return_volatility_decline_fraction"]=None
    return out

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("csv", type=Path, help="user-supplied daily BTC close CSV; see data/SCHEMA.md")
    ap.add_argument("--allow-different-sample", action="store_true", help="skip v0.8 n/date-range enforcement")
    ap.add_argument("--output", type=Path, help="optional JSON output path")
    args=ap.parse_args()
    df=load_data(args.csv, require_frozen_shape=not args.allow_different_sample)
    fit=fit_powerlaw(df)
    lag1=float(np.corrcoef(fit.residuals[:-1],fit.residuals[1:])[0,1])
    eps=strict_episodes(df,fit.residuals)
    ep=episode_analysis(df,fit)
    cur_start=pd.Timestamp(ep["episodes"][-1]["start"])
    cur_start_i=int(df.index[df.date==cur_start][0])
    result={
        "sample":{"n":len(df),"first":str(df.iloc[0].date.date()),"last":str(df.iloc[-1].date.date()),"genesis":str(GENESIS.date())},
        "baseline":{"A":fit.A,"B":fit.B,"R2":fit.r2,"residual_sd_sample":fit.residual_sd_sample,"residual_lag1_autocorrelation":lag1,"residual_lag1_convention":"Pearson correlation of adjacent residual pairs r[t-1], r[t]","naive_se_B":fit.naive_se_B,"hac365_se_B":hac_se_B(df,365)},
        "sampling_robustness":sampling_robustness(df),
        "expanding_B":expanding_B(df),
        "episodes":ep,
        "current_path":current_path_stats(df,fit,cur_start_i),
        "refit":refit_analysis(df,fit,cur_start_i),
        "persistence":persistence_summary(df,fit.residuals),
        "recovery_clock":recovery_clock(df,fit.residuals,eps[:-1]),
        "trend_and_returns":trend_and_return_context(df,fit),
        "trend_volatility_context":trend_volatility_context(df,fit),
    }
    txt=json.dumps(result,indent=2,sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(txt+"\n")
    print(txt)
    return 0

if __name__=="__main__": raise SystemExit(main())
