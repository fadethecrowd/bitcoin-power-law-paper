"""Declared settings for the v0.9 robustness study.

Everything a reader needs to re-run the study with identical random draws is
fixed here: the frozen-sample identity, the model conventions, the declared
null family, the test battery, the alternative (declining-exponent) designs
and every random seed.
"""
from __future__ import annotations

import pandas as pd

# ---------------------------------------------------------------- sample ----
FROZEN_SHA256 = "ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f"
FROZEN_FIRST = pd.Timestamp("2010-07-17")
FROZEN_LAST = pd.Timestamp("2026-08-14")
FROZEN_N = 5873
GENESIS = pd.Timestamp("2009-01-03")      # t = days since genesis (fixed origin)
B_FULL_V08 = 5.650938373388452            # v0.8 full-history exponent (ln P on ln t)

# ------------------------------------------------------------- windows ------
POST_START = pd.Timestamp("2017-01-01")   # "post-2017" expanding start
ROLL_YEARS = (4, 5, 6, 8, 10)             # rolling window lengths (calendar years)
# A rolling window ending on date e holds every close dated after e - L years, up to e.
NAMED_ENDS = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31", "2025-12-31", "2026-08-14"]
YEAR_STARTS = [f"{y}-01-01" for y in range(2011, 2023)]   # start-date sensitivity grid
HALVINGS = ["2012-11-28", "2016-07-09", "2020-05-11", "2024-04-20"]

# ------------------------------------------------------- null family --------
# Deviations u_t (natural-log price units) around a constant-exponent trend:
#   u_t = s * [ sqrt(1-w) * P_t / sd(P) + sqrt(w) * C_t / sd(C) ]
# P: persistence component, C: stochastic four-year cycle, both driven by
# innovations whose scale follows the observed annual return volatility
# raised to the power lam.  s rescales each path so that the residual SD of
# the constant-B least-squares fit equals the observed value (0.69709).
PERSISTENCE = [
    ("ar0.990", "ar", 0.990),   # half-life  69 days
    ("ar0.995", "ar", 0.995),   # half-life 138 days
    ("ar0.997", "ar", 0.997),   # half-life 231 days (matches observed lag-1 ACF)
    ("ar0.998", "ar", 0.998),   # half-life 346 days
    ("ar0.999", "ar", 0.999),   # half-life 693 days
    ("rw", "rw", 1.0),          # random walk: no reversion
    ("frac0.6", "frac", 0.6),   # fractional integration, d = 0.6
    ("frac0.9", "frac", 0.9),   # fractional integration, d = 0.9
]
CYCLE_WEIGHTS = (0.0, 0.4, 0.8)    # share of deviation variance carried by the cycle
CYCLE_PERIOD_YEARS = 4.0           # Harvey trigonometric cycle period
CYCLE_HALF_LIFE_CYCLES = 3.0       # cycle correlation envelope halves after 3 periods
VOL_SHAPES = (0.0, 1.0)            # lam: 0 = constant volatility, 1 = observed profile
SENSITIVITY_VARIANTS = [           # run only for models that pass the screen
    {"tag": "lam0.5", "lam": 0.5},
    {"tag": "lam1.25", "lam": 1.25},
    {"tag": "P3.5", "period": 3.5},
    {"tag": "P4.5", "period": 4.5},
]

# ----------------------------------------------------------- simulation -----
MASTER_SEED = 20261025
STAGE = {"screen": 1, "calibrate": 2, "power": 3, "hac": 4, "asym": 5, "sens": 6, "skew": 7, "critval": 8}
N_CALIBRATE = 1000      # paths per null model (screen + calibration share these draws)
N_POWER = 1000          # paths per (noise model, shape); common random numbers across deltas
N_HAC = 300             # paths per model for interval coverage / unit-root behaviour
N_ASYM = 400            # paths per model for quantile-regression asymmetry
BOOT_REPS = 200         # moving-block bootstrap replicates inside each HAC path
SCREEN_ALPHA = 0.01     # a model is "plausible" if every screening feature has two-sided p >= this

# ------------------------------------------------------------ alternatives --
# Local exponent beta(x) = d ln trend / d ln t, x = ln t.
#  "linear": beta(x) = B + D*(1/2 - (x - x0)/(x1 - x0))   (declines by D across the sample)
#  "late":   beta(x) = B for t < 2017-01-01, then falls linearly in x by D by the cutoff
DELTAS = (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0)
SHAPES = ("linear", "late")
ALPHA = 0.05
