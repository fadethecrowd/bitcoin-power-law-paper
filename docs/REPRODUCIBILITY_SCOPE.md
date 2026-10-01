# Reproducibility scope and conventions

This repository separates three different ideas that are often conflated.

## 1. Exact frozen-file verification

If a researcher already possesses the exact frozen v0.8 CSV, `scripts/verify_exact_frozen_file.py` checks its whole-file SHA-256. This is byte identity, not a statistical test.

## 2. Deterministic statistical reproduction

`scripts/reproduce_v08.py` recomputes the principal deterministic v0.8 quantities from a user-supplied CSV. With the private frozen file it reproduces the core fit, the implemented expanding-window checkpoints, strict episode inventory/ranks, local-depth measures, refit decomposition, rolling persistence summaries, recovery clock, trend hurdles and rolling-return occupancy calculations.

Key conventions are:

- natural logarithms;
- `t = (date - 2009-01-03).days`;
- unweighted OLS with free intercept;
- full-history residual SD uses sample SD (`ddof=1`);
- lag-1 residual autocorrelation is the Pearson correlation of adjacent residual pairs `r[t-1]` and `r[t]` (not the no-intercept sum-form AR coefficient);
- trailing local residual SD uses population SD (`ddof=0`);
- trailing four-year local statistics use the calendar interval `[t-4 years, t)` and therefore exclude the day being scored;
- strict below-trend episodes are consecutive days with residual `< 0`, retaining runs of at least 60 days;
- historical episode residuals use the frozen full-history fit as a common ex-post yardstick;
- the episode-start frozen fit uses data strictly before the first day of the current episode;
- HAC/Newey-West uses a Bartlett kernel, lag 365 and no finite-sample correction for the published 0.18916 slope SE;
- weekly robustness uses Sunday-ending weekly samples; monthly robustness uses the last completed daily observation in each calendar month;
- future trend-hurdle calculations use 365.25 days per year;
- historical rolling CAGRs use calendar-year endpoints (start date plus the stated number of years);
- era labels for rolling windows are assigned by window start date;
- rolling AR(1) windows use 730, 1,461 and 2,191 observations for the 2y, 4y and 6y diagnostics respectively;
- volatility-time recovery is cumulative absolute daily log return after an episode trough through the final below-trend day, and coefficient of variation uses population SD;
- return-volatility context uses 730 daily log returns, population SD (`ddof=0`), annualized by `sqrt(365)`.

## 3. Stochastic-method reproduction

The audited v0.8 record reports a 1,000-rep moving-block bootstrap and a 300-rep constant-true-B structural-break null. The original random-number seeds were not preserved with the scratch scripts.

`scripts/stochastic_checks.py` reconstructs the documented algorithms and calibration and fixes a **new publication-reconstruction seed, 20261001**. Therefore:

- deterministic real-data statistics such as the BIC break locations and segment slopes reproduce exactly to the published precision on the private frozen file;
- regenerated Monte Carlo percentiles should be in the same substantive region but are not promised to equal the exact archived random draw sequence;
- the audited original stochastic outputs are retained in `expected/v0.8_expected_results.json` for comparison.

This limitation is intentional and explicit. The repository does not claim bit-for-bit reproduction of stochastic scratch work whose original seed/state no longer survives.

## 4. What this public reconstruction does not implement

The surviving paper/audit record contains several secondary results whose original scratch implementations were not preserved and which are **not** reconstructed here. In particular, this repository does not claim executable reproduction of:

- the episode-level H1 Spearman `~+0.14`, depth-controlled recovery regression, or leave-one-out sensitivity;
- the reported four-year era-average persistence range `0.9961–0.9974` and corresponding `~177–266 day` half-life summary;
- the separate no-lookahead episode-start diagnostic reported as October 28 / 291 days;
- the 3-day and 7-day zero-crossing bridge robustness checks;
- the `-1.579` cross-denominator comparison;
- the original figure-generation pipelines. The figure files here are raster publication renders/crops, not regenerated from daily source tables.

These omissions do not imply those paper values are false; they mean the surviving materials are insufficient to claim an exact public implementation of those particular calculations.

## 5. Phillips-Perron discrepancy

The v0.8 paper reports a Phillips-Perron `Zt = -2.380` that does not reject a unit root. The original PP scratch code was not preserved. During publication reconstruction, a standard public implementation produced a materially different statistic. Because the implementation choice behind the archived value cannot now be established, `scripts/stationarity_checks.py` **does not recompute PP**. It reports the archived v0.8 value and marks the discrepancy unresolved. A future paper revision/re-audit should settle this explicitly.

## 6. Different-sample mode

The default commands enforce the exact v0.8 sample shape. `--allow-different-sample` is provided only to let readers run the code on lawfully obtained alternative or shorter series. Fixed-date summaries are emitted only when their required checkpoints exist. Results from a different sample are methodological comparisons, not exact reproductions of v0.8. The structural-break null calibration is computed from the supplied monthly series rather than silently reusing the frozen v0.8 calibration.
