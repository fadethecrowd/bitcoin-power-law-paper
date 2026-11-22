# Round 3 referee checks and 12-model non-oracle ablation (2026-11-22)

**Status: exploratory; no change to published v0.9.** The user-supplied Round 3 referee ZIP contains 3 files (README, `round3_checks.py`, `round3.json`) and reports numerical checks on **five lambda=0** models, not an independent full 12-model peer-review verdict. We executed the script against the prior reproducibility bundle: Q0 exact reproduction of model-specific and conditional outputs (max difference **0**), Q1 additivity error **3.997e-15**, and Q2/Q4 numerical cells exactly reproduced. The prior source suite **33/33 tests** passed. This is same-seed reproduction, **not fresh-seed external replication**.

## New model-aware statistical challenge

The referee's matched-checkpoint covariance-aware linear detector yields **49.56%** D=1 10-year detection for `ar0.990|cyc0.8|lam0`, versus **7.12%** with the prior corrected innovation score. It is not universally better: linear D=1 ten-year detection across the other four lambda=0 models was **17.36%, 14.12%, 8.48%, 7.68%**. Whole-ten-year empirical false-alarm rates for this linear test were near 5%, and cutoff calibration/evaluation used separate simulations.

**Blocking interpretation caveat:** `round3_checks.py` gives the detector historical feature `(e.P @ h)[1]` — the fitted slope of *latent simulated noise*, equivalently synthetic estimated exponent minus the *known generating population exponent*. This quantity is unobservable from live BTC prices unless one assumes the true structural exponent is known. It therefore acts as an oracle-like conditioning variable. It is incorrect to describe this as an operationally practical detector, or as universally Neyman–Pearson optimal for the simulator's mixed/scaled noise distributions.

We ran a fresh-seed ablation **across all 12 models**, using synthetic-training 1,400, disjoint calibration 1,600, and disjoint evaluation 1,200 histories per model. It conditions only on observable pre-onset OLS residuals at days 0,30,91,182,365,730,1461 before monitoring begins, excluding hidden generating slope error. Ten-year D=1 model-specific detection then ranged **7.0–78.4%** compared with **6.8–98.9%** with the hidden slope-error feature. Model-specific ten-year null alarms were **3.25–5.17%** without the feature; D=1 two-year detection was **1.75–5.50%**. Examples:
- AR(.990) cycle .8 lambda=0: D1 ten-year **50.8% with** latent slope error, **28.2% without**.
- AR(.990) cycle .8 lambda=1: **98.9% with**, **78.4% without**.
- AR(.995) cycle .4 lambda=1: **51.9% with**, **20.6% without**.
- mixed RW cycle .4 lambda=1: **6.8% with**, **7.5% without**.

Thus *some* correctly specified model-aware tests are much more powerful than previous heuristics, but not robust to unknown residual families.

## Unknown-family stress test

A detector trained on just AR(.990) cycle .8 lambda=0, using **only observable historical residuals**, was calibrated at a conservative 10-year, full-path 5% false-alarm budget *over all 12 null families*, with Bonferroni marginal bounds, 1,000 calibrations and 700 independent evaluations/model. D1 ten-year detection was **0–7.3%** across models (versus **0–3.3%** for a comparable EWMA); observed null alarm fractions were **0–3.1%** for the linear score. This is **not a bound on all adaptive or mixture detectors**: it deliberately stress-tests one post-hoc selected working model and a worst-family threshold.

Future volatility sensitivity: under AR(.990) lambda=1, observable-only D1 ten-year detection fell from **78.4%** with 2025 completed-year future volatility to **72.8%** with the mean 2023–25 completed-year estimate; AR(.995) lambda=1 fell **20.6% → 18.9%**, and mixed RW lambda=1 remained **7.5%**. Hence even large model-aware gains depend on future noise assumptions.

## Pure Gaussian RW theorem — narrow qualification

At known age 6,432d, sigma=.0219/day, D=1, alpha=.05 one-sided fixed-horizon, independently computed optimal simple-hypothesis power: **7.17% at 2y, 9.64% at 10y, 10.94% at 20y, 14.11% as H→∞**. This follows from the square-summable innovation shifts `-D*log((age+t)/(age+t-1))`; it is **not** the numeric power ceiling for Bitcoin or the mixed RW+cycle model. It also assumes an exactly known baseline trend, onset and innovation model. The stationary-AR contrast does not automatically transfer when the pre-break trend must be estimated from finite history.

## Scientific conclusion and remaining blockers

1. Fitted exponent is directly price-derived, not independent evidence of a true underlying structural exponent; strong historical fit != structural identification != prospective change-detection accuracy.
2. **Do not claim** a general 10-year detection upper bound from previous EWMA/innovation results. Covariance-informed detectors can be markedly stronger in some known models.
3. **Do not claim** model-aware 78% detection is available to live users; true residual model, true exponent and break onset are not known.
4. Validate a genuinely model-family-adaptive, non-oracle, unknown-onset algorithm with simultaneous state-conditional error control; test alternate forward volatility and full generator distribution match.
5. Request a fourth targeted referee decision challenging the latent slope-error feature, observable-only covariance detector, cross-family conservative threshold and finite-information theorem.

A complete **licensed-price-free** reproducibility archive is prepared in this research session with all source/aggregate outputs, the third referee replay, new ablation and a targeted fourth-review brief. Only this diagnostic note is committed to the branch; the previous paper release remains frozen.
