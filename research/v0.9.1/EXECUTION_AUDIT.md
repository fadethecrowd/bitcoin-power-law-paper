# v0.9.1 execution audit — 2026-11-21

Status: **Step 1 inspection completed; Step 2 reproducibility check partially verified from repository artifacts; new computation NOT executed.**

## Inspected repository sources
- `v09_robustness/README.md`: run instructions, data policy, frozen data hash, reproducibility policy.
- `v09_robustness/requirements.txt`: pinned dependencies.
- `v09_robustness/lib/config.py`: original generator, seed, volatility/cycle and persistence declarations.
- `v09_robustness/lib/nulls.py`: generator and alternative trend construction.
- `v09_robustness/scripts/04_power.py`: historical retrospective power test, separate calibration/evaluation draws.
- `v09_robustness/outputs/plausible_models.json`: original plausible-model screen, 12 models of 48.
- `expected/v0.9_expected_results.json`: frozen provenance and published target metrics.
- `research/v0.9.1/monthly_exponents.py` and `research/v0.9.1/DIAGNOSTIC_01.md`: already-committed exploratory diagnostic.

## Verified from repository (not independently rerun in this pass)
- Frozen sample SHA256: `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`
- 5,873 daily closes from 2010-07-17 through 2026-08-14, genesis 2009-01-03.
- Published B = 5.6509383734.
- v0.9 historical simulation master seed `20261025`. Do **not** modify it to implement the new research.
- v0.9 screened-model family includes near-unit-root AR(1), fractionally integrated and RW variants, including both constant-volatility and observed-volatility-profile versions.
- Published package pins Python 3.12+ and NumPy 2.5.3, SciPy 1.18.1, Pandas 3.0.5, statsmodels 0.15.0, matplotlib 3.11.2, arch 8.0.0, pytest 9.1.1.

## Critical engineering issues identified
1. `Generator` currently simulates from genesis to the sample endpoint and accepts a `df` with historical annual return-volatility values. Forward extensions need explicit future-volatility rules specified **without looking at realized future prices**.
2. `Generator.draw` rescales each simulated path using its full-sample detrended SD; when extended beyond the vintage date, that can unintentionally make forecast-period volatility or future trajectory enter the calibrated forecast. Define calibration-time-only scaling or a precommitted predictive simulation calibration protocol.
3. `04_power.py` tests *looking-back* rejection statistics and does not measure sequential first-alarm times. A new forward-simulation runner is required; retroactive power results cannot serve as prospective detection proof.
4. The P10 definition must distinguish pointwise conditional predictive distribution (persistent residuals, parameter uncertainty) from historical residual quantiles. A raw in-sample residual 10th percentile is not automatically a 10th-percentile 4-year-ahead forecast.
5. P10 vintages at 4 years require an explicit cutoff; fewer independent 4-year forecast windows exist than overlapping monthly forecast dates imply.
6. The frozen private file was confirmed in an earlier exploratory diagnostic, but it was **not mounted or reprocessed during this pass**. Published aggregate results alone are not an independent rerun.
7. Claude's proposed synthetic best-case detection probabilities are to be reproduced, not accepted as validated results.

## Execution decisions (pre-simulation)
- Original v0.9 source/output stays untouched.
- Continue on `research/v0.9.1-stability-detection`.
- New results in `research/v0.9.1/`, with new configuration and new stage seeds distinct from historical v0.9 stages.
- Primary screened family: all 12 models in `v09_robustness/outputs/plausible_models.json`.
- Detection primary alternative D={0.5,1.0,3.0}; sensitivity D={0.4,0.65}; step and 2/4-year ramps, anchored continuously at change date.
- False alarm target: probability of at least one alarm over 10 future years <=5%; sensitivity 1% and 10%.
- Simulation horizons 5/10/20 years; report resolution at 50% and 80% power, censor nondetections.
- P10 historical vintages evaluated separately at 1/2/4-year endpoints; distinguish endpoint breaches from any-breach measures.
- No significance claims until model extensions, seed configuration, and leakage controls are implemented and tested.

## Remaining prerequisites before confirmatory run
1. Freeze the fully specified P10 predictive-quantile construction, burn-in date, monitoring start, detector feature definitions, future volatility assumption and handling of parameter uncertainty.
2. Implement explicit simulation-only smoke tests verifying constant-B, zero-D equivalence, no future leak, horizon handling, and family-wise first-alarm size.
3. Confirm access to the private frozen data file *locally* for full deterministic reproduction.
4. Execute published regression tests with pinned environment and frozen series, checking output hashes.
5. Record versioned configuration and SHA256 checksums, and seal a commit **before** viewing new empirical output.

## Note on claims
This audit is a repository-source inspection and acceptance checklist, not completed empirical verification. Do not mark Step 2 complete until automated checks actually run.
