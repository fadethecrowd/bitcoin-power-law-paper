# Diagnostic 05 — Different-class innovation-score detector

**Run date:** 2026-11-22. **Status:** exploratory; 12-family synthetic study, not empirical proof of a Bitcoin structural break. The private licensed price CSV is **not** included here or in reproducibility artifacts.

## Motivation / referee response

Claude's reproduction found that the 180-day EWMA can be weak and that starting residual conditions its false-alarm risk. We tested a genuinely distinct approach rather than another smoothing window: a **one-sided score based on AR(0.997)-whitened forecast-gap increments**, weighted against the signed shape of a unit exponent decline. The AR(.997) is deliberately fixed for all 12 models; for non-AR(.997), fractional, cyclical and RW models it is *not* a correctly specified likelihood-ratio detector. Because this is a non-oracle but **known monitoring-onset** template, it is not a universal operational break detector.

The score is observed at predeclared future checkpoints (1,2,5,10 years); an alarm occurs if any checkpoint score exceeds a constant calibrated upper cutoff. Comparison: the earlier 180-day EWMA gap monitor with an any-time lower crossing threshold. Each uses the **same 10-year full-surveillance 5% false-alarm target**, with model-specific thresholds estimated on independent simulations. No real future BTC prices were used.

## Ten-year results

- Sample: 12 originally screened v0.9 residual processes, 1,000 synthetic calibration histories **plus 1,000 disjoint evaluation histories per model**. Historical generated residuals matched to published pre-onset v0.9 detrended log-residual SD with **historical-only** scaling. Future volatility assumption: last complete year held fixed for lambda=1.
- Empirical null false-alarm fractions: innovation score **3.1–4.7%**, EWMA **2.9–5.6%**; none is a joint simultaneous guarantee of <=5% due to Monte Carlo uncertainty.
- For a real local-exponent decline of **D=1.0**, detection within 2 years: innovation **0–2.3%**, EWMA **0–2.4%**. Detection within 10 years: innovation **6.8–16.2%**, EWMA **6.0–13.0%**.
- For a larger **D=3.0**, 10-year detection: innovation **17.8–60.2%**, EWMA **15.3–56.0%**.
- The two methods were calculated from the same evaluation paths within each model and D, allowing paired comparisons. The innovation detector sometimes improves 10-year sensitivity, but not universally; **its early-detection performance is still poor**.

## Conditional false alarms

Splitting the 1,000 evaluation histories by initial *pre-onset OLS fitted residual* (below -0.5, between -0.5 and +0.5, above +0.5) reproduces a serious issue. Among the first five lambda=0 screened models, the innovation detector mostly falsely alarms for starts above +0.5, with rates of roughly **8–21% conditional on starting above +0.5**. For lambda=1 and non-AR models the dependence varies substantially. Unconditional 5% calibration is therefore **not a 5% conditional promise** for any given starting state. We cannot use this detector to give an individual live warning without conditioning or explicitly acknowledging conditional size.

## Twenty-year exploratory extension

The same two monitoring rules were independently calibrated to a **20-year full-surveillance budget** and evaluated at checkpoints 2/5/10/20 years, 350 calibration histories and 350 independent evaluation histories per model. This is a low-precision feasibility check, NOT a reliable estimate of 20-year power or statistical size:

| D | Innovation 20-year detection range | EWMA 20-year detection range |
|---:|---:|---:|
| 0 / null | 1.7–6.6% | 2.0–6.6% |
| 1 | 7.4–21.7% | 6.6–20.9% |
| 3 | 32.6–96.0% | 25.4–98.0% |

At least one observed null alarm fraction **exceeded 5%** in this small holdout; no inferential 20-year result should be published from it. Surveillance cutoffs were re-estimated for the 20-year horizon; the earlier 10-year thresholds were **not** reused.

## Validation and limitations

Five local unit tests passed for the innovation-score implementation (zero, deterministic score, shift direction, no future-to-past score leakage, distinctness from EWMA). All 12 models ran. These are **local** simulations with NumPy/SciPy installed in the research environment, not a pinned complete rerun of published v0.9, and they have not yet been reviewed independently.

Technical limitations:
- Whitened score assumes an AR(0.997)-style working correlation even when it is false; its alternative onset and drift template are known in advance.
- Per-path historical detrended residual scaling remains a modeling condition inherited from v0.9. The limited referee sensitivity checks have not been extended to all 12 models.
- Model-specific threshold assumes the residual family is identified in advance; an across-family score-specific threshold and fully state-conditioned calibration are still required.
- Checkpoint innovation alarm and continuous EWMA monitor have different monitoring frequencies despite matching the whole-horizon false-alarm budget. The comparison is informative but not a clean equal-surveillance-frequency test.
- Fixed-start 2026-08-14 forecasts are not repeated at unknown onset dates. We do not have general onset-agnostic change detection.
- For the present current Bitcoin market: **no test here establishes that the true exponent changed**.

## Next gates

1. Conditionally calibrate and independently validate the false-alarm budget by initial residual state (and initial slope error if relevant), including minimum-bin path counts.
2. Repeat the 10y detector comparison with **matched monitoring calendars** and use an across-family threshold whose whole-path size is externally verified.
3. Increase the 20y calibration/validation sample dramatically, then measure 50%/80% resolution delays with uncertainty.
4. Complete the remaining independent v0.9 full-distribution matching and parameter-scale sensitivity, and obtain a second referee review before any sweeping inference.
5. LinkedIn public description should say: *We are studying why detecting deterioration in Bitcoin's fitted Power Law may be harder than a high historical R² suggests. Our exploratory tests find strong dependence on assumed price noise and detector design.* Do **not** claim no practical test exists.
