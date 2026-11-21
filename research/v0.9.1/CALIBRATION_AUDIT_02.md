# Calibration audit 02 — original v0.9 residual family and forecast-start conditioning
Date: 2026-11-21. **Engineering audit, not a detection result.**

## Exact frozen-data verification
Working copy of original licensed series was checked against SHA-256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`.
Reproduced on 5,873 daily closes: B=5.650938373388459, residual SD=0.6970880734627248.

## Past-only future volatility assumption
The published `v09_robustness/lib/nulls.py` constructs day-specific innovation volatility from historical observed annual log-return standard deviations. For a forward path starting after 2026-08-14 the realized future volatility is unknown. Two explicitly historical forecasting assumptions were inspected:
- Hold 2025 (last fully completed calendar year) daily log-return SD fixed into forecast: 0.02192479255.
- Hold mean of 2023, 2024 and 2025 annual daily log-return SD fixed: 0.02415699217.
Their difference is ~10.2%; model with lambda=0 is unaffected. These are volatility *shape* inputs, not a claim that actual future volatility will be stable.

## Prototype synthetic calibration benchmark
A local, uncommitted Python calibration prototype used original model persistence/cycle shapes, normalizations based on *past-sample-only Monte Carlo*, 35 pre-onset calibration paths per model and 30 independent evaluation paths per model. The historical dispersion target was 0.697088. Results indicate why **forecast-start conditioning is essential**:
- Under the random-walk+cycle model, a 30-path pilot's simulated forecast-start residual SD was about 2.65 log units even though the original historical **detrended residual SD** target was only 0.697.
- AR+cycle onset-level SD also differed substantially by model and volatility assumption (~0.38–0.91 in the same trial).
- The historical OLS free intercept/slope partly absorb pre-onset accumulated noise, and a prospective alarm must define what part of the starting residual state is known and conditioned on. Blindly comparing `u_future` to a fixed global zero-residual trend produces spurious first alarms, especially for a random walk.
- The reference v0.9 generator normalizes *each entire simulated historical path* by its fitted detrended SD. This is acceptable as a retrospective null device but cannot simply be extended through the future and normalized on future draws.

**Consequence:** this 35×30 exercise is a debugging/scale audit only. It is not a calibrated reproduction of the v0.9 screened family's distributions and **no structural-break detection rates are published from it**.

## Required correction and tests before power estimates
1. Record observation-time fitted trend and residual state from the simulated pre-onset path. Calibrate the alarm against the *same vintage-estimation procedure* under null and alternative; do not assume the true pre-onset trend/intercept is known in realistic detectors.
2. For simple diagnostics, examine `u(t)-u(t0)` and conditional predictive deviations, but **do not** assume this anchoring alone replaces refitting the historical regression.
3. Preserve AR, random-walk, fractional and cycle latent state across forecast start. Keep historical-scale and future-volatility rules independent of actual future observations.
4. Run equivalence tests for each family against v0.9's historical null statistics (especially ACF, amplitude ratio and detrended residual SD), not merely exact seeds/horizon-invariance.
5. Freeze the final detector and compare family-wise first-alarm size on independent calibration/evaluation draws; only then report power and resolution horizons.

## Scope
This audit is directly about the paper's structural-identifiability question. P10 remains a secondary retrospective-lower-band check. Published v0.9 is unchanged.
