#!/usr/bin/env python3
"""Reconstructed stochastic checks for the v0.8 paper.

Important: the original August 2026 scratch scripts and RNG seeds were not
preserved. The algorithms and calibration below are reconstructed from the
frozen paper and adversarial verification report. The fixed publication-reconstruction seed
is therefore a *new* reproducibility convention, not a claim about the seed
used for the published Monte Carlo draws.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from reproduce_v08 import load_data, fit_powerlaw

PUBLICATION_RECONSTRUCTION_SEED = 20261001


def slope(x,y):
    xc=x-x.mean(); yc=y-y.mean()
    return float(np.dot(xc,yc)/np.dot(xc,xc))


def moving_block_bootstrap(df, block_days=365, reps=1000, seed=PUBLICATION_RECONSTRUCTION_SEED):
    x=np.log(df.days_since_genesis.to_numpy(float)); y=np.log(df.price_usd.to_numpy(float)); n=len(x)
    rng=np.random.default_rng(seed)
    starts_max=n-block_days+1
    nblocks=math.ceil(n/block_days)
    vals=np.empty(reps)
    offsets=np.arange(block_days)
    for b in range(reps):
        starts=rng.integers(0,starts_max,size=nblocks)
        idx=np.concatenate([s+offsets for s in starts])[:n]
        vals[b]=slope(x[idx],y[idx])
    return {
        "block_days":block_days,"reps":reps,"publication_reconstruction_seed":seed,
        "median_B":float(np.median(vals)),"sd_B_sample":float(np.std(vals,ddof=1)),
        "q025":float(np.quantile(vals,.025)),"q975":float(np.quantile(vals,.975)),
    }


def monthly_xy(df):
    m=df.set_index('date').resample('ME').last().dropna().reset_index()
    return m, np.log(m.days_since_genesis.to_numpy(float)), np.log(m.price_usd.to_numpy(float))


def detector_factory(x, min_len=12, max_breaks=4):
    n=len(x); sx=np.r_[0,np.cumsum(x)]; sxx=np.r_[0,np.cumsum(x*x)]
    def detect(y):
        sy=np.r_[0,np.cumsum(y)];syy=np.r_[0,np.cumsum(y*y)];sxy=np.r_[0,np.cumsum(x*y)]
        cost=np.full((n,n),np.inf);slp=np.full((n,n),np.nan)
        for i in range(n):
            js=np.arange(i+min_len-1,n)
            if len(js)==0: continue
            nn=js-i+1; X=sx[js+1]-sx[i];Y=sy[js+1]-sy[i];XX=sxx[js+1]-sxx[i];YY=syy[js+1]-syy[i];XY=sxy[js+1]-sxy[i]
            den=XX-X*X/nn; b=(XY-X*Y/nn)/den; a=(Y-b*X)/nn
            sse=YY+a*a*nn+b*b*XX+2*a*b*X-2*a*Y-2*b*XY
            cost[i,js]=sse;slp[i,js]=b
        candidates=[]
        for K in range(max_breaks+1):
            S=K+1;dp=np.full((S+1,n),np.inf);prev=np.full((S+1,n),-1,int)
            dp[1,min_len-1:]=cost[0,min_len-1:]
            for s in range(2,S+1):
                for j in range(s*min_len-1,n):
                    ks=np.arange((s-1)*min_len-1,j-min_len+1)
                    vals=dp[s-1,ks]+cost[ks+1,j]
                    q=int(np.argmin(vals));dp[s,j]=vals[q];prev[s,j]=int(ks[q])
            sse=dp[S,n-1]
            bic=n*math.log(sse/n)+(2*S)*math.log(n)
            ends=[n-1];jj=n-1
            for s in range(S,1,-1): jj=prev[s,jj];ends.append(jj)
            ends=sorted(ends);starts=[0]+[e+1 for e in ends[:-1]]
            slopes=np.array([slp[i,j] for i,j in zip(starts,ends)])
            candidates.append((bic,K,starts,ends,slopes))
        bic,K,starts,ends,slopes=min(candidates,key=lambda z:z[0])
        return {"K":K,"starts":starts,"ends":ends,"slopes":slopes,
                "max_adjacent_slope_change":float(np.max(np.abs(np.diff(slopes)))) if len(slopes)>1 else 0.0,
                "slope_range":float(np.ptp(slopes))}
    return detect


def structural_break_check(df,reps=300,seed=PUBLICATION_RECONSTRUCTION_SEED):
    monthly,x,y=monthly_xy(df); detect=detector_factory(x)
    real=detect(y)
    break_dates=[str(monthly.date.iloc[s].date()) for s in real['starts'][1:]]
    true_B=slope(x,y)
    true_a=float(y.mean()-true_B*x.mean())
    monthly_resid=y-(true_a+true_B*x)
    rho=float(np.corrcoef(monthly_resid[:-1],monthly_resid[1:])[0,1])
    resid_sd=float(np.std(monthly_resid,ddof=0))
    innovation_sd=resid_sd*math.sqrt(max(0.0,1-rho*rho))
    rng=np.random.default_rng(seed);Ks=[];adj=[];ranges=[]
    for _ in range(reps):
        e=np.empty(len(x));e[0]=rng.normal(0,resid_sd)
        for t in range(1,len(x)): e[t]=rho*e[t-1]+rng.normal(0,innovation_sd)
        sim=detect(true_a+true_B*x+e);Ks.append(sim['K']);adj.append(sim['max_adjacent_slope_change']);ranges.append(sim['slope_range'])
    adj=np.asarray(adj);ranges=np.asarray(ranges);Ks=np.asarray(Ks)
    return {
        "publication_reconstruction_seed":seed,"reps":reps,"monthly_n":len(monthly),"null_rho":rho,"null_residual_sd":resid_sd,"null_true_B":true_B,
        "real":{"selected_K":real['K'],"break_dates":break_dates,"segment_slopes":[float(z) for z in real['slopes']],"max_adjacent_slope_change":real['max_adjacent_slope_change'],"slope_range":real['slope_range']},
        "null":{"K_counts":{str(k):int(np.sum(Ks==k)) for k in range(5)},
                "max_adjacent_median":float(np.median(adj)),"max_adjacent_q95":float(np.quantile(adj,.95)),"max_adjacent_q99":float(np.quantile(adj,.99)),
                "real_max_adjacent_percentile_empirical":float(np.mean(adj < real['max_adjacent_slope_change'])),
                "p_null_ge_real_max_adjacent":float(np.mean(adj >= real['max_adjacent_slope_change'])),
                "slope_range_median":float(np.median(ranges)),"real_slope_range_percentile_empirical":float(np.mean(ranges < real['slope_range'])),
                "p_null_ge_real_slope_range":float(np.mean(ranges >= real['slope_range']))}}


def ar1_first_passage_demo(reps=4000, seed=PUBLICATION_RECONSTRUCTION_SEED):
    rho=0.99699
    sigmas=[0.85,0.55,0.31]
    def run(start_mode, sigma, offset):
        rng=np.random.default_rng(seed+offset)
        start=-0.82 if start_mode=="raw" else -2.0*sigma
        x=np.full(reps,start,dtype=float);active=np.ones(reps,dtype=bool);times=np.full(reps,np.nan)
        innovation_sd=sigma*math.sqrt(1-rho*rho)
        for t in range(1,10001):
            inds=np.flatnonzero(active)
            if len(inds)==0: break
            x[inds]=rho*x[inds]+rng.normal(0,innovation_sd,len(inds))
            hit=x[inds]>=0
            times[inds[hit]]=t;active[inds[hit]]=False
        return float(np.nanmedian(times))
    raw=[run("raw",s,10+i) for i,s in enumerate(sigmas)]
    std=[run("std",s,110+i) for i,s in enumerate(sigmas)]
    return {"publication_reconstruction_seed":seed,"rho":rho,"reps_per_regime":reps,"sigmas":sigmas,"same_raw_start_minus_0_82_median_days":raw,"same_standardized_start_minus_2_sigma_median_days":std,"note":"Numerical illustration only; standardized first-passage law is analytically scale-invariant at fixed rho."}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('csv',type=Path);ap.add_argument('--seed',type=int,default=PUBLICATION_RECONSTRUCTION_SEED);ap.add_argument('--quick',action='store_true');ap.add_argument('--output',type=Path);ap.add_argument('--allow-different-sample',action='store_true',help='skip v0.8 n/date-range enforcement')
    args=ap.parse_args();df=load_data(args.csv,require_frozen_shape=not args.allow_different_sample)
    boot_reps=200 if args.quick else 1000; break_reps=50 if args.quick else 300
    out={
      "notice":"Reconstructed algorithms with a new fixed publication-reconstruction seed; original August 2026 RNG seeds were not preserved.",
      "moving_block_bootstrap_365":moving_block_bootstrap(df,365,boot_reps,args.seed),
      "structural_break_null":structural_break_check(df,break_reps,args.seed),
      "ar1_scale_invariance_demo":ar1_first_passage_demo(1000 if args.quick else 4000,args.seed),
      "audited_v08_stochastic_targets":{"bootstrap_365_sd_B":0.2401,"bootstrap_365_q025":5.0466,"bootstrap_365_q975":5.9960,"break_null_K4_share":0.997,"break_real_max_adjacent_percentile":0.547,"break_real_slope_range_percentile":0.590},
      "audited_v08_deterministic_break_targets":{"real_max_adjacent_slope_change":13.9335,"real_slope_range":16.5848}
    }
    txt=json.dumps(out,indent=2,sort_keys=True);print(txt)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(txt+'\n')

if __name__=='__main__': main()
