# v0.9.1 Diagnostic 03 — matched-family forward-detection experiment (exploratory)
**Run:** 2026-11-22. **Status:** complete exploratory simulation; NOT confirmatory evidence of a real-world break or the impossibility of detection.

## Central question
Can a real decline in Bitcoin's *local exponent* be distinguished from ordinary, strongly persistent price deviations without generating frequent false alarms? This experiment examines **one predeclared class of practical monitoring rule** across all 12 originally screened v0.9 null models.

## Design
- Input is the exact privately held frozen series, SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`, 5,873 observations ending 2026-08-14. The published full-history OLS exponent was reproduced as 5.650938373388456 and detrended log-residual SD as 0.6970880734627248.
- Matched v0.9 historical residual generator: AR(1) rho 0.990/.995/.997/.998/.999, fractional integration d=.9 and random walk; corresponding stochastic-cycle weights .4/.8; historical annual-return volatility profile and per-synthetic-history **historical-only**, detrended residual normalization. The latter matches the retrospective v0.9 null distribution without using future realizations to set simulated scale.
- Future innovation volatility for lambda=1 held at last **completed** calendar year, 2025 (daily return SD 0.02192479255). For lambda=0 constant innovation volatility. This is a research assumption, not a forecast.
- Each synthetic history has its historical Power Law fitted by free-intercept OLS before the start of the simulated future. The forward score is the 180-day-half-life EWMA of `(future log price - pre-onset fitted log trend) - (last historical log price - pre-onset fitted log trend)`: a baseline anchored to the observed starting residual. True local exponent changes are introduced continuously as `-D log(t/t0)`; D in {0,0.5,1,3}.
- One-sided lower alarms. Per-model threshold is the 5th percentile of the *whole 10-year minimum* score over 2,000 calibration paths. The conservative across-family threshold is the minimum of all 12 model thresholds. Independent random seeds and 2,000 fresh evaluation histories per model/alternative. Horizon results use first hit by 1/2/5/10 years. Each model has its own equally weighted evaluation for audit; model averages are NOT interpreted as a posterior probability for Bitcoin.

## Key observations: detection rates across 12 models (range, percentages)
| D | Model-specific 2y | Model-specific 10y | Across-family 2y | Across-family 10y |
|--:|--:|--:|--:|--:|
| 0 (false alarms) | 0.1–2.1 | 3.9–6.65 | 0–0.4 | 0–3.9 |
| 0.5 | 0.1–2.45 | 4.8–8.85 | 0–0.4 | 0–4.8 |
| 1.0 | 0.1–2.75 | 6.4–14.95 | 0–0.45 | 0–6.4 |
| 3.0 | 0.15–5.2 | 16.15–63.45 | 0–0.5 | 0.4–16.15 |

With this rule, the effective 10-year detection power for D=1 exceeds the model-specific null false-alarm rate by only a modest amount. A common worst-family threshold can be even less informative.

**Important size caveat:** model-specific independent-evaluation 10-year null alarm rates range 3.9–6.65%, with at least one above nominal 5%. Do NOT claim independently verified 5% control for every per-model threshold. With finite calibration and evaluation samples this requires a further precision check or conservative adjustments. In this exploratory run the common worst-family threshold produced ≤3.9% observed null alarms for all evaluated models.

## Validation: matching v0.9 historical null structure
- A separate 400-synthetic-history/model comparison used **the same exact ACF definition** as `v09_robustness/lib/stats.py`: `dot(e[:-lag],e[lag:])/dot(e,e)`. The initially attempted Pearson subseries correlation was identified as a different statistic and replaced before comparison.
- Across all 12 models, difference between fresh and published v0.9 screening medians was at most 0.0002 at lag 1, 0.0261 at lag 365 and 0.0191 at lag 1461. These are reasonably close Monte Carlo medians from *different sample sizes and seeds* (400 vs original 1000), but **not** complete equivalence testing of all seven screened features.
- Seven engineering tests passed, including exact sample identity, deterministic seeds, no horizon-prefix leakage across all 12 models, no future volatility leaking into historical draws, exact pre-onset SD, D=0 equivalence and forecast score prefix invariance.
- A prior initial-state RNG defect was fixed in `forward_family.py` and fixed independently in the local matched-history runner.
- This numerical work was performed on NumPy 2.3.5 / SciPy 1.17.0 / pandas 2.2.3, **not** the published pinned v0.9 environment; no claim of byte-for-byte reproduction of the full v0.9 package.

## Interpretation
These findings concern **the 180-day EWMA forecast-error rule**, not all possible detectors. Its weak performance is consistent with the idea that the historical Power Law parameters are weakly identified for future break detection in a highly persistent process. It does NOT establish that no more powerful detector exists, nor prove the actual Bitcoin exponent changed. The prior *known-onset, known-process Gaussian likelihood-ratio* benchmark answers a different question and must not be compared directly with unknown-onset full-path alarms as if they used equal assumptions.

## Work remaining
1. Verify all original screening features, especially zero crossings, cycle-band share, and volatility/amplitude ratios, and test future-volatility sensitivity (2025 vs mean 2023–25).
2. Compare *multiple predeclared* detection rules (shorter/longer EWMA, likelihood-based AR controls, rolling slope), and ensure equal **family-wise whole-path** false-alarm budgets.
3. Re-run with pinned dependencies and additional independent random seeds, and implement confidence intervals / finite-calibration uncertainty for tail size.
4. Extend onset and ramp scenarios, and evaluate 20-year resolution.
5. Only after these gates assess implications for paper wording.

Raw licensed prices, synthetic daily histories, and individual-price-reconstructing output are **not** committed to the repository.

## Follow-up robustness check, same day
A second, smaller **600 calibration / 600 evaluation paths per model** run compared two predeclared future-volatility assumptions: (a) 2025 daily log-return volatility held fixed (0.02192479), and (b) the mean of completed 2023–25 annual volatilities held fixed (0.02415699). The common worst-family threshold was identical in these same-seed runs at -2.7409 because a lambda=0 model determined it; D=1 ten-year family-threshold power ranged 0–9% for either assumption, and model-specific D=1 ten-year power ranged 6.0–15.5% (2025) versus 6.0–15.17% (three-year mean). This is a limited sensitivity comparison, not evidence that volatility forecasts do not matter more generally.

**Critical size qualification:** in both 600-path runs, the observed *maximum* family-threshold ten-year null alarm share was 6.83%. The 2,000-path run yielded 3.9% maximum. This inconsistency is compatible with Monte Carlo variation but means that **even the across-family threshold must not yet be described as empirically proven to control the false alarm probability at 5%**. A larger independently seeded calibration/evaluation test, or an explicit conservative threshold with a confidence-bound size guarantee, is required.

A downloadable reproducibility bundle accompanying this research turn contains the local Python simulation runner, unit tests, and aggregate results; the GitHub report alone is not a full executable reproduction of the new experiment. The original private licensed daily series was not included.
