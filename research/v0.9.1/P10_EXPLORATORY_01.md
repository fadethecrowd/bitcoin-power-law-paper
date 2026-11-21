# Historical vintage P10 exploratory pass — 2026-11-21

**Status: exploratory, not a calibrated P10 inference.** This file contains only summary statistics, no licensed daily prices.

## Reproducibility and integrity
- Original frozen 5,873-row CSV located in private file library and materialized locally.
- Three versions of the named frozen CSV have matching SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`.
- Independent log-log OLS on original CSV recovered B=5.650938373388459, intercept=-37.71919344501603, residual SD=0.6970880734627248.
- Research code: `vintage_p10.py`, `test_vintage_p10.py`. 5 tests passed. In all, 12 unit tests across this pilot and `sequential_pilot.py` passed locally.
- Default simulation Python environment: NumPy 2.3.5, SciPy 1.17.0, Pandas 2.2.3; **not** the published pinned v0.9 environment. The published 11-stage robustness suite has not been independently rerun here.

## Prospective construction (illustrative, not yet a validated quantile)
- First eligible calendar month-end: 2017-01-31; refit log price to log days since genesis using all prices available **through the vintage only**.
- Exactly 1, 2, 4 calendar years after each vintage, using that future endpoint's completed daily close.
- 'Marginal P10': vintage fitted trend plus z_0.1 times vintage in-sample residual SD. **Not** a full predictive quantile, neglects intercept/slope uncertainty and residual dependence.
- 'Conditional P10': AR(1) persistence rho=0.997 applied to vintage last residual with predictive diffusion variance using vintage residual SD; ignores uncertainty in persistence, trend and residual-scale estimates.
- Changing a 2020+ future portion of a synthetic series left 2018-vintage predictions and observed 2019 errors unchanged. Duplicate/missing date and nonpositive-price checks passed.
- These endpoint breaches are **not** probability of crossing the band at any time in the forecast horizon.

## Frozen actual data: endpoint fractions
| Forward horizon | Eligible overlapping monthly vintages | Marginal P10 breached | Conditional P10 breached |
|---|---:|---:|---:|
| 1 calendar year | 103 | 2/103 = 1.94% | 6/103 = 5.83% |
| 2 calendar years | 91 | 0/91 = 0.00% | 0/91 = 0.00% |
| 4 calendar years | 67 | 2/67 = 2.99% | 2/67 = 2.99% |

**Do NOT compare directly to 10% as if the vintages were independent or the thresholds were calibrated quantile forecasts.** Adjacent vintages overlap dramatically; several breaches may arise from one drawdown, and this vintage construction's predictive calibration is unknown.

## Synthetic AR(1) check (100 independent paths/model)
Fixed trend B=5.650938373388459, intercept=-37.71919344501603, residual stationary SD=0.6970880734627248. AR(1) rho separately 0.995, 0.997, 0.999; 100 simulation paths each; same vintage algorithm and burn-in, seed 20261122. Only *marginal* P10 comparison below.

| rho | horizon | mean breach share over synthetic paths | 5th–95th percentile of synthetic per-path breach shares |
|---|---|---:|---:|
|0.995|1y|17.59%|1.94%–35.10%|
|0.995|2y|18.84%|1.10%–41.81%|
|0.995|4y|20.34%|0.00%–49.25%|
|0.997|1y|20.16%|0.97%–43.74%|
|0.997|2y|22.16%|0.00%–51.76%|
|0.997|4y|24.27%|0.00%–62.99%|
|0.999|1y|24.16%|0.00%–55.63%|
|0.999|2y|27.01%|0.00%–64.95%|
|0.999|4y|32.12%|0.00%–89.70%|

Even under these simplified reference processes, the per-history coverage range is wide. The observed endpoint shares are on the *low* side in this comparison, but **this is not enough to conclude P10 is conservatively calibrated**: sample dependence, model screening, nonstationarity, full vintage uncertainty and volatility/cycle structures remain to be addressed. Only 100 simulations per AR model means the tail quantiles are noisy.

## Pending before inferential interpretation
1. Implement v0.9 screened 12-model family with future-volatility extrapolation and calibrated predictive-quantile definitions.
2. Distinguish conditional predictive P10 from retrospective 10% residual quantiles using a precise statistical target and estimated uncertainty.
3. Aggregate by distinct drawdown as well as monthly forecast vintage and formally simulate the entire overlapping test.
4. Confirm results with pinned dependencies, an independent seed, and higher simulation counts.
5. Keep the known 2025–26 drawdown as an exploratory stress scenario, not a fresh independent holdout.
