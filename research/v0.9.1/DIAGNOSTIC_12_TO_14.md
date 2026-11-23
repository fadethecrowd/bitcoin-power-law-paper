# Diagnostics 12–14 — Identification, matched detectors, unknown onset and robust-size audit

**Date:** 2026-11-22. **Status:** EXPLORATORY / referee review pending. **Published v0.9 remains frozen**; no licensed daily prices, daily observed residuals, or fitted daily price series are posted to this repository.

## Core identification finding

In an expanding log-price-on-log-age OLS regression with an intercept, the incremental fitted slope is a deterministic transformation of that day's price forecast error and leverage:

`Bhat_n - Bhat_(n-1) = ((n-1)/n) (x_n-xbar_(n-1)) / Sxx_n * (y_n - ahat_(n-1) - Bhat_(n-1)*x_n)`.

This is an exact OLS update formula—not a claim that fitted slopes are useless predictors. Checked numerically for 5,508 expansions, max absolute error **5.15e-14**. A fitted-slope decline is **not independent observational confirmation** of a changed latent structural exponent.

## Diagnostic 09 held-out score audit

Original 12-family synthetic held-out NPZ scores (2,500 null calibration, 2,000 evaluation histories/model) recomputed from source:
- Posterior-weighted: mean null 5.10%, D=1 10y detection **18.38%**, AUC **0.6786**.
- Historically selected: 5.02%, **16.82%**, AUC **0.6617**.
- Privileged true-residual-family-identity comparator: 5.32%, **20.96%**, AUC **0.6884**.

Paired conditional bootstrap for weighted minus oracle identity: AUC −0.00979 (95% CI −0.01316 to −0.00653), power −2.59 percentage points (95% CI −3.06 to −2.14). CIs condition on models and fitted/calibrated rules, not real-world BTC model uncertainty.

## Diagnostic 12: paired, same-time endpoint detector comparison

12 original screened null families; per family 500 score training / 2,500 disjoint calibration / 2,000 disjoint evaluation, plus volatility and cycle stress paths. Compare ridge-regularized pre-onset-feature-informed linear score against downside 180d EWMA at identical 2y or 10y terminal decision times. Under model-specific nominal ~5% null sizes:

| Horizon | Linear mean size/power D1 | EWMA mean size/power D1 |
|---|---:|---:|
| 2 years | **5.18% / 7.59%** | **5.07% / 6.42%** |
| 10 years | **5.07% / 18.55%** | **5.31% / 14.48%** |

10y mean AUC **0.69185** (linear) versus **0.64024** (EWMA). Paired 300-bootstrap D1 detection improvement **+4.07pp**, conditional 95% CI **+3.62 to +4.62pp**. These rules use *different historical feature sets*, and model-specific cutoffs assume the true family is known.

**Unknown-family calibration:** conservative common cutoffs with one-sided Clopper–Pearson/Bonnferroni over 12 families×4 endpoint rules yield mean null **0.90%** (linear) / **1.06%** (EWMA) and mean D1 power **2.12% / 2.49%** at 10y; worst-family holdout null **4.25% / 4.30%**. The low achieved size is important; do not present low power as a fundamental limit.

Future-only +50% volatility in non-break histories makes worst-family false alarms **8.25% / 7.33%**. Calibration against baseline/+25%/+50% future volatility reduces baseline null to **0.13%** and D1 power to **0.34% / 0.33%**. Future-only cycle-period stress (4y to 3.5/4.5/5y) produces up to **6.0%** worst-family size for ridge with 5y period.

## Diagnostic 13: true daily unknown-onset CUSUM

A causal one-sided Page CUSUM and continuously inspected EWMA operate daily without knowledge of break onset, with 10y whole-path calibration. Across 12 families and 1,800 null calibration + 1,400 disjoint evaluation histories/model:
- Model-specific ~5% size: CUSUM mean size **5.05%**, D1 detection **17.26%**; EWMA **5.24%**, D1 **11.16%**.
- Conservative single familywide cutoff: mean size **0.64%/0.87%**, D1 alarms **1.29%/1.58%**; some alarms in post-break scenarios occur **before** actual change, so are not true detections.
- +50% unmodeled future volatility: worst-family false alarm **6.8%/9.8%**.
- State effect of unconditional calibration: worst observed within-state-model null **10.34%** (CUSUM) / **8.85%** (EWMA).

## Diagnostic 14: predeclared state-specific robust threshold

Starting-state bins residual <−0.5, [−0.5, +0.5], >+0.5, with simultaneous one-sided Clopper–Pearson/Bonferroni tolerance allocation across **72** family×state×detector cells. Shared thresholds depend only on state, not on knowing the true family; fresh evaluation seeds 1,400 paths/model. Baseline mean null **0.21% CUSUM / 0.35% EWMA**, mean D1 power **0.48% / 0.55%**; worst observed baseline conditional null **2.44% / 3.41%**. Under +50% unmodeled future volatility, one EWMA state-model cell had **6.61%** false alarms. Highly conservative calibration imposes a severe sensitivity cost; not evidence no better detectors exist.

## Generator fidelity and independent reproduction

Adapted original v0.9 generator vs current forward generator: 600 historical null paths/model/engine; 9 marginal scalar features×12=108 two-sample KS comparisons, **zero Bonferroni rejections**, but **does not prove full joint distribution equivalence**. Original 5,873-row frozen file SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f` confirmed.

A private referee ZIP prepared for the user includes **only non-reconstructing 17 annual volatility summaries and published aggregate OLS/residual scale** rather than licensed BTC prices. An aggregate-only simulation adapter generated bit-identical paths against the complete-CSV engine for 12 families×3 seeds, and an aggregate-only end-to-end smoke pilot replicated source-file engine results. This does not independently audit annual aggregate accuracy or the original v0.9 pinned environment. Do not upload the user's private ZIP or its derived-calibration file publicly without explicit permission.

Unit suite **13/13 passed**; direct online CUSUM invariants and future-only-cycle equivalence checked. Full results, source and review brief supplied separately to user for independent Claude referee handoff; **not yet independently refereed**.

## Scholarly scope and next gate

These are *synthetic* tests of hypothetical post-2026-08-14 exponent changes, **not** evidence Bitcoin's exponent actually declined. Historical fit, structural mechanism, and prospective break-detection ability must not be conflated. Do not claim structural falsification is impossible or that the v0.9 Power Law is permanent.

**Remaining:** external adversarial code/method review; original published v0.9 generator pinned environment check; larger state-conditioned holdouts; calibration under truly out-of-family volatility, jumps and cycles; compare predictors beyond simple fitted exponent. LinkedIn: qualitative scientific question only, no definitive synthetic rate claims.
