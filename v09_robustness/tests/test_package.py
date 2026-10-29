"""Checks for the v0.9 robustness package.

1. Reproduction targets (run only when outputs/reproduction.json came from the
   exact frozen file): the v0.8 and October 2026 review numbers.
2. Output policy (always): nothing in outputs/ is a daily-resolution series.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
ISO = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")


def rep():
    p = OUT / "reproduction.json"
    if not p.exists():
        pytest.skip("run scripts/01_reproduce.py first")
    d = json.loads(p.read_text())
    if not d.get("frozen_match"):
        pytest.skip("reproduction.json was not produced from the frozen v0.8 file")
    return d


def test_baseline():
    d = rep()
    assert abs(d["baseline"]["B"] - 5.650938373) < 1e-8
    assert abs(d["baseline"]["hac365_se"] - 0.18915992) < 1e-7
    assert d["baseline"]["fast_nw_matches_statsmodels"]
    assert abs(d["post2017_B"] - 4.864547) < 1e-6


def test_rolling_and_decomposition():
    d = rep()
    r5 = d["rolling_B"]["5y"]["named"]
    assert [r5[k] for k in ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31", "2025-12-31", "2026-08-14"]] == \
        [6.3028, 4.9215, 4.7765, 4.2004, 3.2648, 4.1151]
    assert d["rolling_B"]["4y"]["named"]["2025-12-31"] == 6.7198
    dec = next(x for x in d["decomposition"] if x["to"] == "2025-12-31")
    assert (dec["daily_shapley_departing"], dec["daily_shapley_arriving"]) == (-2.0297, 1.0941)


def test_break_detector_v08():
    d = rep()["break_detector"]
    assert d["fast_detector_matches_reference"]
    assert d["selected_K"] == 4
    assert (d["max_adjacent_slope_change"], d["slope_range"]) == (13.9335, 16.5848)


def test_outputs_contain_no_daily_series():
    for f in OUT.glob("*"):
        if f.suffix not in {".json", ".csv"}:
            continue
        dates = set(ISO.findall(f.read_text()))
        assert len(dates) < 60, f"{f.name} holds {len(dates)} distinct dates; daily series are not allowed"
        if f.suffix == ".json":
            def walk(o):
                if isinstance(o, list):
                    assert len(o) < 200, f"{f.name}: list of length {len(o)}"
                    for v in o:
                        walk(v)
                elif isinstance(o, dict):
                    for v in o.values():
                        walk(v)
            walk(json.loads(f.read_text()))


def test_phillips_perron_replacement_values():
    """v0.9 replaces the unreproducible v0.8 PP value (-2.380) with arch 8.0.0 values."""
    d = rep()["unit_root"]
    assert d["pp_lag11_const"] == -3.0416
    assert d["pp_auto_const"] == -3.3072
    assert d["v08_reported_pp"] == -2.38


def test_unitroot_critical_values_present():
    import csv
    p = OUT / "unitroot_critical_values.csv"
    if not p.exists():
        pytest.skip("run scripts/11_unitroot_critical_values.py first")
    rows = {r["statistic"]: r for r in csv.DictReader(p.open())}
    # constant-volatility random walk: simulated 5% values close to residual-based tables
    for r in rows.values():
        assert -3.45 < float(r["const_vol_5pct"]) < -3.25
        assert float(r["btc_vol_5pct"]) < -4.0


def test_epoch_extremes_are_not_reconstructive():
    """Epoch residual extremes: no dates, at most 2 decimals (data-redistribution policy)."""
    p = OUT / "reproduction.json"
    if not p.exists():
        pytest.skip("run scripts/01_reproduce.py first")
    for e in json.loads(p.read_text())["halving_epochs"]:
        assert set(e) == {"epoch", "start", "end", "complete", "max_resid_ln", "min_resid_ln"}, e
        for k in ("max_resid_ln", "min_resid_ln"):
            assert round(e[k], 2) == e[k], (e["epoch"], k, e[k])
