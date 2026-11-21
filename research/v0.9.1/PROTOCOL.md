# v0.9.1 — exponent deterioration, detection lag, and real-time band reliability
Status: **research protocol / NOT a completed empirical result**  
Prepared: 2026-11-21  
Base: published v0.9 (2026-10-29), DOI 10.5281/zenodo.23774503.

## Research question
Can a sustained change in the local Bitcoin price-age exponent be distinguished from a *constant-exponent* trend plus persistent, cyclical, and heteroskedastic deviations early enough to be practically useful? How reliable is the P10 lower band in a genuinely real-time / out-of-sample setting?

## Preserve v0.9
- Do not modify, refit, or silently replace published v0.9 coefficients, simulations, figures, tests, or conclusions.
- Frozen training series: 5,873 completed UTC daily closes, 2010-07-17 through 2026-08-14; genesis date 2009-01-03; free-intercept unweighted OLS in log-log space.
- Frozen v0.9 baseline: A=4.1568315435e-17, B=5.6509383734, sample residual SD=0.6970880735. **Do not conflate this B with older dashboard coefficients 5.69705.**
- Extended analysis: **distinct** strictly completed UTC daily-close series through a named cutoff no later than 2026-11-20; record provider, UTC conventions, missing-day checks, input hash and whether data are exact-frozen or independently reconstructed.
- Price input is private / provider licensed; never commit daily close series, daily residuals or files from which daily prices can be reconstructed. Aggregate results and reproducible source code only.
- Intraday lows are descriptive events, never observations in regressions fitted to completed UTC closes.

## Deferred improvements carried forward for review
Earlier v0.9 review deferred (1) model-specific confidence-interval calibration and (2) higher break-count caps. Treat as **provisional** v0.9.1 carryovers pending comparison with earlier editorial notes, not as a verified complete prior v0.9.1 specification.
- Revisit interval coverage under the declared persistence-model family, report each model and family-wide conservative coverage.
- Vary structural-break maximum count, including beyond the previous cap; recalibrate size and power under constant-B simulations. Higher detected break counts without null calibration are not evidence of exponent change.

## Work packages
### A. Real-time expanding and rolling exponent diagnostics
1. Refit expanding samples at every month-end (first sample date and minimum sample length explicitly recorded). Also calculate 3-, 5-, 7-, and 10-year rolling window estimates where feasible; rolling is descriptive, **not a standalone hypothesis test**.
2. Plot point estimates plus **null-calibrated simultaneous envelopes** from the preserved constant-B residual families; account for scanning many months/windows.
3. Tabulate duration and magnitude of decreasing estimates (3/6/12/24 months) and how frequently *the same pattern occurs under a constant exponent*. Analyze values using a common calendar endpoint; distinguish a new low from a persistent downward slope.
4. Study sensitivity to start date, time origin held fixed at genesis, residual model, volatility specification, sample end, and departing-versus-arriving observations in rolling windows.

### B. Define and calibrate a 'sustained decline' alarm
Use three illustrative horizons (3–6 months watch; four quarters warning; two years candidate). These are **unvalidated monitoring windows**, not statistical rejection criteria. Pre-specify and then calibrate joint alarm rules based on:
- change in expanding-window estimate vs its simulated simultaneous confidence envelope;
- negative slope / cumulative movement across multiple consecutive months;
- independent evidence from recent-window exponents and persistent negative residuals;
- stability across residual-model families.
Select thresholds by simulated **false-alarm probability**, including whole-history and 10-year family-wise risk (target 5% and sensitivity 1%, 10%), not by post-hoc choosing a dramatic price episode. Report unconditional and conditional-on-current-low diagnostics separately.

### C. Detection-power and lag experiment (primary new contribution)
Simulate bitcoin-length price histories on the exact daily time grid under:
- constant B null with plausible and sensitivity residual families from v0.9;
- exponent shifts/declines of total size D in {0.30, 0.60, 0.90, 1.50} plus the earlier v0.9 stress values up to D=3;
- gradual declines with 1-, 2-, 4-, and 6-year ramps, and abrupt slope changes;
- starts at multiple historic dates and recent dates, without conditioning away unfavorable realizations.
Parameterize changes in **local log-price/log-age derivative** and integrate to create continuous alternative trends; document clearly because a mere change in an exponent applied to unanchored t^B can spuriously jump the intercept.
Calibrate alarms on disjoint null simulations and evaluate on independent simulation draws. For each alternative report power within 6, 12, 24, 36 and 60 months; median / p10 / p90 first-detection lag among detected runs; probability of missed detection; false alarms under null; model-family worst-case outcomes. Explicitly evaluate whether 12–24 month detection is *achievable* rather than promising that it is.

### D. P10 / below-trend reliability
- Define P10 mathematically and distinguish fixed-original-model P10, recursively refitted P10, and any empirically quantile-calibrated band; don't equate the three.
- Compute breaches on **completed UTC closes** and summarize 1/7/30/60/90-day consecutive-run episodes, maximum depth, cumulative log deficit, and recovery (return above the specified band).
- For every historical month-end fit, freeze the parameters before looking ahead; report forward coverage and frequency/duration of breaches with explicit dependence and overlapping-horizon corrections.
- Test whether underperformance of real-time P10 is more compatible with a stationary persistent residual process, a near-unit-root process, volatility changes, or true exponent deterioration.
- A nominal P10 is a cross-sectional 10th-percentile threshold under a distributional model, **not** a guaranteed price floor and not necessarily a 10% probability of one or more breaches over a multi-year period.

### E. Competing growth / forecast test
Compare fixed-B v0.9 to flexible local-slope, piecewise and gradual-decay models, plus persistent-residual nulls. Use strictly forward-chaining windows; compare 6-, 12-, 24- and 36-month log-price accuracy and predictive interval coverage. Penalize complexity and report benchmark performance under the null. Do not select models by performance on the final holdout before evaluating them.

### F. Retirement-model impact (separate application, not a model selection criterion)
- Preserve the user's existing dashboard / P10 calibration separately. Do not substitute v0.9's B=5.650938 into the dashboard model B=5.69705 or vice versa without explicit reconciliation.
- Show illustrative time-anchored lower-B sensitivities and uncertainty, without presenting them as empirically calibrated forecasts.
- Discuss how an unrecognized long-lived structural break affects P10-based retirement planning. Do not make portfolio changes or automatically revise dashboard values.

### G. Independent November 2026 paper
Claude's comparison is pending. Record the paper's exact URL, author, publication date and algorithm; compare dataset time convention, regression start, monthly refit schedule, frozen real-time band definitions and tests. Distinguish established prior art / convergence from any allegation of copying, which requires evidence beyond similar method.

## Analysis conventions / acceptance criteria
- All v0.9 outputs preserved and reproduced first (or clearly mark no exact private CSV available).
- Scripts with dependency lock, fixed random seeds, command examples and automated tests.
- Predeclare alarm thresholds and model grids before viewing extended-window results; label any retrospective exploration as exploratory. Replicate with alternative seed.
- Show per-model null and alternative operating characteristics; don't pool screened and unscreened models without labeling.
- Report simulation uncertainty intervals and uncertainty from selecting the residual family on the same observed data.
- Audit for look-ahead leakage, overlapping test windows, regression intercept/exponent identification, and multiple comparisons.
- Provide figures: expanding/rolling B with simultaneous null envelopes; alarm false-positive / detection-lag curves; P10 forward coverage; residual regime comparisons; sensitivity table.
- Deliver an aggregate-only methodology/results report, machine-readable aggregate summary and short proposed paper addendum. **No significance, detection-lag claim, or revised band should be reported until the code is run against verified input.**

## Immediate execution status (2026-11-21)
- Retrieved and inspected v0.9 README and robustness methodology from main.
- Drafted research protocol on a separate branch; **no v0.9 code changed, no simulations or price ingestion run, and no v0.9.1 empirical results established yet**.
