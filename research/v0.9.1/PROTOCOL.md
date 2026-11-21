# Bitcoin Power Law v0.9.1 — Revised Research Protocol (2026-11-21)

**Status:** protocol revision; no new confirmatory result. Supersedes the broader v0.9.1 protocol drafted earlier today following independent design review. The earlier exploratory diagnostic is retained, clearly labeled exploratory.

**Published baseline (IMMUTABLE):** v0.9, 2026-10-29, DOI 10.5281/zenodo.23774503. Original 5,873 UTC closes, 2010-07-17 to 2026-08-14; time origin Bitcoin genesis 2009-01-03. Published free-intercept OLS coefficients A=4.1568315435e-17, B=5.6509383734, sample residual SD=0.6970880735. Private frozen dataset SHA-256: `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`. Dashboard calibration B=5.69705 is a **different model** and must not be substituted. No daily licensed prices/residuals are to be committed.

## Scope priority clarified 2026-11-21

**Primary scientific objective:** identify the statistical distinguishability of a change in the underlying local log-price/log-age growth exponent from a constant exponent plus highly persistent deviations. Inference about growth-law validity and the identifiability of structural change is the paper's central claim. No retirement-dashboard analysis is part of this research.

**Secondary bounded methodological audit:** real-time P10 vintage testing is retained only to assess whether retrospective lower-band statements in published v0.9 suffer from hindsight conditioning. It is not intended to design a retirement forecast, optimize P10, or turn this paper into a downside forecasting paper. Reserve detailed predictive-quantile calibration as separate follow-up if it becomes a substantial independent workstream.

**Important experimental distinction:** a fixed-horizon simple-versus-simple optimal detector with *known* onset, alternative and noise parameters is a useful idealized benchmark for detection power, but is not a calibrated sequential alarm. Report its assumptions and compare it to realistic detectors, without treating the known-alternative result as a universal upper bound for misspecified or composite tests.

## Decision and hypotheses

We **do not assume** that a 12–24 month early-warning system is feasible. A decline in expanding-window B is not in itself evidence of a change in the *local* forward growth exponent. We will quantify how slowly genuine changes can be distinguished from persistent residual deviations and, separately, whether vintage P10 is calibrated as a forecast quantile.

The primary estimands are:
1. Forward **time to first alarm**, its false-alarm distribution under constant-B null processes, and power under specified local-slope alternatives.
2. **Resolution horizon**: time until 50% and 80% power for a specified shift, at a controlled false-alarm budget; censor runs not detected within simulation horizon.
3. Vintage **P10 point-forecast quantile coverage** at fixed 1-, 2-, and 4-year horizons, and distribution of breach depth/duration at those horizons, versus the identically executed procedure in simulated constant-B histories.

These are distinct from probability of **any** breach during a horizon, which can substantially exceed 10%.

## Confirmatory guardrails and experiment boundaries

- This revised protocol must be committed **before** subsequent simulations or analysis of any newly extended 2026 price observations. Already seen 2025–26 drawdown and the earlier exploratory rolling diagnostics invalidate an independent retrospective test on that episode: label all such results exploratory.
- Use *only* the published frozen series for the primary historical analysis. An extended series to a named complete UTC close, with provider/hash checked, may be a separately labeled sensitivity study, not tuning data. Distinguish Bitstamp from frozen CryptoCompare/CoinGecko data; never silently splice sources.
- Genesis clock, log transform, intercept convention, vintage availability date, missing-day rule, sample burn-in, definition of P10, residual models, seeds, grids, detector thresholds and competing-model list must be frozen in configuration **prior** to running relevant confirmatory jobs. If any cannot be verified from existing code, stop and document the choice as pending rather than improvise after examining outcomes.
- Existing published v0.9 simulation families and their screening are the starting point. Do not select only the most favorable residual model. Report per-model results and worst-case family performance separately. Preserve uncertainty in baseline B and fitted residual parameters when specified.
- Calibration and evaluation simulations must use **disjoint seeds and draws**. Calibrate monitoring thresholds on null simulations, never on the observed breach. Report Monte Carlo binomial intervals for detection and coverage metrics.
- Multiple vintages, multiple lookahead days and breach episodes are dependent. Do not use naïve independent-binomial or uncorrected Kupiec/Christoffersen tests as decisive evidence. Explicitly report distinct drawdowns as well as breach observations; calculate simulation-based reference distributions.
- Every model-selection or exploratory deviation after protocol freeze must be logged and labeled. No claiming that a detector 'predicted' the known 2025–26 episode.

## Package A — Sequential detection feasibility (new, not a rerun of v0.9)

**Null:** constant local exponent B with the pre-existing v0.9 screened residual processes (including high-persistence and declining-volatility variants where licensed inputs can be run locally). Constant-B simulations generated on the original daily calendar and projected forward 5, 10, and 20 years.

**Alternatives:** continuous, time-anchored structural changes to local slope `d(log trend)/d(log age)`: a step to B-D and a linear ramp over 2 or 4 years. Primary D grid: 0.5, 1.0, 3.0; decision-relevant sensitivity D=0.4, 0.65. Because onset is post-freeze, maintain continuity by integrating local slope from onset; no discontinuous re-scaling of `t^B` without an anchored intercept. Include constant-B null in the identical run.

**Detectors:** (1) frozen-vintage-trend residual CUSUM; (2) one-sided sequential likelihood-ratio / cumulative deficit detector where an explicit likelihood is valid; (3) expanding-window B outside the historical 5.5–6.0 band only as an illustrative comparator, not a calibrated scientific alarm. If detector 2 is invalid for a given residual family, report inapplicability instead of forcing it.

**False-alarm calibration:** null first-alarm probability at most 5% over a 10-year monitoring horizon (sensitivity: 1% and 10%). Evaluate whole monitoring path, not per-check significance; use separate simulations for threshold choice and evaluation. Report expected waiting time and null first-alarm distribution; show family-robust and individually calibrated detectors explicitly.

**Outputs:** 5/10/20-year detection delay CDFs, rates of false alarm and missed detection; horizon when power reaches 50% and 80%; uncertainty for those estimates; and smallest D excluded/identified at each future vintage under declared assumptions. No predefined 12–24 month success target. If even 80% power for D=1 requires >5 years, describe 'early warning' as unsupported under the tested assumptions, not as a universal impossibility proof.

## Package B — Real-time P10 calibration (primary empirical contribution)

1. Use historical month-end **vintages** after an explicitly frozen burn-in; report all vintages as a sensitivity, to expose vintage-selection effects. Before each forecast, fit the specified power-law trend using **only prices through that vintage**.
2. Predeclare whether P10 is a Gaussian-log-residual quantile, empirical expanding-window residual quantile, or a separately stress-calibrated prospective quantile. These definitions must not be pooled. If empirical quantile estimation is used, estimate with past observations only; never copy the all-history multiple forward or backward.
3. Evaluate the log-price at fixed **1-, 2-, and 4-year endpoints** relative to the respective vintage P10 predictive threshold, subject to genuinely available future data. The quantile definition must specify whether uncertainty in fitted coefficients and residual persistence is included. Evaluate at the exact horizon endpoint; separately report fraction of days below the **vintage-projected path** over that horizon.
4. Report observed vintage-level breach frequencies, coverage by vintage cohort, maximum depth, duration and recovery definitions; distinguish a single drawdown causing many dependent breaches from many independent failures.
5. Run the **identical vintage estimator + forward evaluation** on disjoint constant-B simulated histories from every screened residual model. Compare observed statistics with simulation reference distributions, not a nominal iid 10% test. Report effective sample and vintage overlapping explicitly.
6. Treat any 'stress floor' as a separate **past-only** calibration; do not transfer Mooij's all-history 0.42x multiple or retrospectively choose 0.30x.
7. Do not infer that a 10% pointwise quantile implies only 10% chance of *any* crossing in a multi-year period.

## Package C — Conditionally triggered model comparison

Run only **if** package B finds material out-of-sample miscalibration beyond simulated constant-B reference ranges. Predeclare one simpler persistence-aware comparator and one gradual local-slope alternative **before** inspecting B results. Use identical vintages and fixed horizons; label overlapping multi-year forecast comparisons low effective-sample. Do not optimize on the 2025–26 event.

## Existing work and exclusions

- v0.9 already contains 4/5/6/8/10-year rolling-window sensitivity and structural-break analyses; **do not repackage or repeat as new evidence**. The exploratory 3/5/7/10-year diagnostic committed today remains descriptive only.
- No arbitrary '3–6-month watch / 4-quarter warning / 2-year break' tiers.
- Mooij's November 2026 independent monthly refits should be cited in contextual comparison. Incorporate the substantive real-time-vintage insight without turning the study into a rebuttal. Similar refits are not evidence of copying.
- Deferred interval calibration and increased break-count caps belong to a separately tracked robustness item; do not quietly add them to a confirmatory v0.9.1 result.
- Retirement/dashboard stress testing is a **separate application**, not evidence of model validity; no dashboard updates, trading decisions or asset changes in this study.
- State-space, general regime models, log-periodic residuals, extensive competitor searches and source-switching are deferred.

## Execution and publication gates

1. **Protocol frozen:** record commit hash and SHA-256 of this file; record simulator code revision and package versions, seeds and explicitly populated configuration. Until these exist, no confirmatory simulation.
2. **Detection feasibility:** run forward simulations on known screened models, checking sensitivity to the residual family. Inspect false-alarm/power tradeoff and resolution horizons.
3. **P10 vintage:** run prospectively defined historic coverage, calibrate null yardsticks via matching simulator, and run dependency checks.
4. **Optional C:** only if B establishes motivation.
5. Publish only aggregate summaries, code that does not expose licensed data, and a transparent analysis log. Published v0.9 untouched. Decide between a small 0.9.1 addendum and companion study **after** results.

## Review provenance

Informed by the user's 2026-11-21 independent Claude reviews of Mooij's 'The Formula, Month by Month' and the proposed v0.9.1 program. Their feasibility-bound numbers are **claims to reproduce**, not confirmed results in this repository. Especially check the assumptions underlying AR(1) rho=0.997 and single-check 5% detection estimates. 
