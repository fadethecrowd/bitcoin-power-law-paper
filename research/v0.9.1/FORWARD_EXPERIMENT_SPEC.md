# v0.9.1 — Forward structural-identifiability experiment: execution specification
Prepared 2026-11-21. **Pre-run engineering supplement** to the revised PROTOCOL.md; not an empirical conclusion.

## Central hypothesis
Observed declines in the *expanding fitted* exponent do not uniquely identify changes in the *local true* exponent. Quantify the delay/false-alarm trade-off for a real continuous change in forward log-price-vs-log-age slope, across the **12 originally screened v0.9 residual families** rather than an arbitrary AR(1) alone.

## Methodological split
1. **Idealized benchmark**: known onset/size/process; `oracle_detection_bound.py` provides fixed-horizon, simple-vs-simple Gaussian power only. It is not a sequential rule, universal information bound, or empirical finding.
2. **Operational detector**: onset and effect size unknown. Calibrate the probability of *at least one* false alarm over ten future years to ≤5%, separately for each original residual family and with a conservative all-family threshold. Use distinct calibration and evaluation seeds. Compute power by 1,2,5,10 and 20 years, first-alarm delay distribution, and 50%/80% resolution horizons.
3. **Observed data**: retain the frozen v0.9 series for fit/validation; label post-2026-08-14 observations exploratory only. No retirement variables or model replacement.

## Residual-family scope (from original screened-model artifact)
- AR(1) rho .990 with cycle weight .8, lambda 0/1
- AR(1) rho .995/.997/.998/.999 with cycle weight .4, lambda 0/1
- Fractional integration d=.9 with cycle weight .8, lambda 1
- Random walk with cycle weight .4, lambda 1
Total = 12. No model may be silently dropped because its forecast behavior is inconvenient. If an engine cannot simulate a family correctly, report it as an unexecuted blocker.

## Required simulation changes
**Original `v09_robustness/lib/nulls.py` must not be reused without adaptation**: it constructs volatility from actual annual return volatility through the fit endpoint and normalizes simulated residuals using full simulated paths. Extending this machinery past the onset without changes can allow future volatility and future residuals to affect forecast-time scale. The new implementation shall:
- estimate any data-based volatility parameters only from historical days available at onset;
- predeclare future volatility extrapolation for lambda=1 (primary: last fully completed calendar year's volatility held fixed; sensitivity: average of last 3 completed years, held fixed); keep lambda=0 constant;
- determine residual-innovation scaling using the pre-onset training interval or pre-calibrated null trials, **never** normalize a simulated path by its future realized standard deviation;
- start each simulated path with a reproducible pre-onset state, including the AR, fractional or random-walk and stochastic-cycle components, rather than forcing noise to zero at the onset without justification;
- implement fractional-memory convolution with preserved pre-onset history; treat RW innovations as non-mean-reverting and state how pre-onset conditioning is handled;
- run reproducible tests: constant-B null, D=0 alternative equality, continuous alternative at onset, truncated-future invariance, no-lookahead volatility, 10-year family-wise false-alarm calibration, seed determinism, and whole-path stopping correctness.

## Alternatives
For a decline in local exponent D anchored at t0, the price-log trend deviation is `-D * log(t / t0)` after an abrupt break. A ramp decline is the time integral of a linearly changing local log/log slope, continuous at onset. Primary D in {0.5,1,3}; decision sensitivity {0.4,0.65}; original trend baseline remains B=5.6509383734. Hypotheses are distinguished through their **forward price-age growth**, not by choosing a fitted expanding-B alarm threshold after observing the 2025–26 prices.

## Detection algorithms: declared before checking results
- Negative cumulative residual / EWMA of log-price gap to frozen-vintage trend: grid of fixed half-lives {90,180,365} days, threshold selected with an across-grid null maximum/minimum to control familywise alarms; report each individually as descriptive.
- Sequential one-sided likelihood-ratio detector in *models with a correctly specified likelihood* (simple AR-only control case); do not assign false likelihoods to fractional or stochastic-cycle mixtures.
- Expanding exponent <5.5 or outside [5.5,6.0]: legacy comparator, **not** a calibrated break-detector.
- Specify a common score normalization using only pre-onset estimates or null-calibration distribution; do not make post-onset normalization adaptive.

## Precision and interpretation
- Initial engineering smoke test: ≤100 simulations per model, **no inferential or detection headline**.
- Confirmatory run target: ≥2,000 null calibration paths per model and ≥2,000 independent evaluation paths per model/alternative; simulations must expose Monte Carlo uncertainty and reproducible seeds. If tail precision is insufficient, increase N before the final report under a predeclared Monte Carlo accuracy rule.
- Distinguish known-onset idealized test from unknown-onset sequential detection. Do not compare numerical power of tests with different whole-path false-alarm budgets as if equivalent.
- Report per-family null alarms, minimum/maximum power, and controls for stochastic cycles and declining volatility. Do not report an average as though the residual family were known.
- If realistic detector power remains low, the scientific finding is a **limit of identifiability under the declared models**, not proof of a genuine exponent change or that all possible tests must fail.

## Gate
Do not label the full 12-family experiment 'executed' until the forward-state generator, forecast-time scaling, smoke tests and predeclared configuration are committed and all pass. Keep P10 as a bounded appendix note to v0.9 historical floor interpretations, not the main research objective.
