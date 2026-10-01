import importlib.util
from pathlib import Path
import math
import pytest
import sys
import os
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts'/'reproduce_v08.py'
spec=importlib.util.spec_from_file_location('reproduce_v08',SCRIPT)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

@pytest.fixture
def frozen_csv():
    # Explicitly opt-in local test path. The public repo never ships the dataset.
    raw=os.environ.get('BPL_FROZEN_CSV')
    if not raw: pytest.skip('set BPL_FROZEN_CSV to run exact frozen-data tests')
    p=Path(raw)
    if not p.exists(): pytest.skip('BPL_FROZEN_CSV path does not exist')
    return p

@pytest.fixture
def frozen(frozen_csv):
    df=mod.load_data(frozen_csv); fit=mod.fit_powerlaw(df)
    return df,fit

def test_baseline(frozen):
    df,f=frozen
    assert len(df)==5873
    assert math.isclose(f.B,5.650938373388455,abs_tol=1e-10)
    assert math.isclose(f.A,4.1568315435335095e-17,rel_tol=1e-10)
    assert math.isclose(f.r2,0.9612807090518647,abs_tol=1e-10)
    assert math.isclose(f.residual_sd_sample,0.6970880734627248,abs_tol=1e-10)
    assert math.isclose(mod.hac_se_B(df,365),0.1891599197097628,abs_tol=1e-9)

def test_current_episode_and_refit(frozen):
    df,f=frozen
    ep=mod.episode_analysis(df,f)
    assert len(ep['episodes'])==10
    cur=ep['episodes'][-1]
    assert cur['start']=='2025-11-03'
    assert cur['duration_days']==285
    assert cur['minimum_raw_date']=='2026-06-30'
    assert math.isclose(cur['minimum_raw_residual'],-0.8165301658207,abs_tol=1e-10)
    assert math.isclose(cur['minimum_local_sigma_depth'],-2.7320709499,abs_tol=1e-8)
    assert math.isclose(cur['cumulative_negative_area_log_days'],136.4816866644,abs_tol=1e-8)
    start_i=int(df.index[df.date==pd.Timestamp('2025-11-03')][0])
    ref=mod.refit_analysis(df,f,start_i)
    assert math.isclose(ref['episode_start_B'],5.7033644380,abs_tol=1e-9)
    assert math.isclose(ref['refit_absorption_log_fraction'],0.0784080757,abs_tol=1e-8)
    assert math.isclose(ref['refit_absorption_price_fraction'],0.1125991090,abs_tol=1e-8)

def test_recovery_clock_and_hurdles(frozen):
    df,f=frozen
    eps=mod.strict_episodes(df,f.residuals)
    clock=mod.recovery_clock(df,f.residuals,eps[:-1])
    assert math.isclose(clock['calendar_time_cv_population'],0.8836223484,abs_tol=1e-8)
    assert math.isclose(clock['volatility_time_cv_population'],0.7401535233,abs_tol=1e-8)
    tr=mod.trend_and_return_context(df,f)
    assert math.isclose(tr['keep_pace_cagr']['1'],0.3663130995,abs_tol=1e-8)
    assert math.isclose(tr['catch_up_cagr']['1'],1.9903752807,abs_tol=1e-8)
    assert math.isclose(tr['catch_up_cagr']['2'],1.0048860477,abs_tol=1e-8)
    assert math.isclose(tr['catch_up_cagr']['3'],0.7461474986,abs_tol=1e-8)


def test_different_sample_helpers_do_not_require_fixed_end_date(frozen):
    df,f=frozen
    short=df[df.date <= pd.Timestamp('2026-02-18')].copy().reset_index(drop=True)
    sf=mod.fit_powerlaw(short)
    tv=mod.trend_volatility_context(short,sf)
    assert '2026-08-14' not in tv['checkpoints']
    assert '2012-12-31' in tv['checkpoints']
    eb=mod.expanding_B(short)
    assert '2026-08-14' not in eb
    assert '2025-12-31' in eb
