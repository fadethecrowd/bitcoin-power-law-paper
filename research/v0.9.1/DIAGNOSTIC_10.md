# Diagnostic 10 — Twelve-model referee tail-mixture: independent-seed replication

**2026-11-22. Exploratory.** Published v0.9 is frozen. Reproduced referee weighted null-tail mixture over all **12** screened v0.9 families using the original frozen Bitcoin dataset for historical-volatility calibration only. The private price dataset was SHA-verified and not published.

## Design and completed execution

Two distinct seed replications. Each: 260 training, 300 first calibration, 300 second calibration, 300 holdout histories per model = **13,920** histories across 12 models, **27,840 combined**. The true local log-age exponent declines by D=0,1,3 at a known onset. Alarms are inspected at years 1,2,5,10. Calibration sets and evaluation sets are disjoint. Both methods use conservative common cross-model thresholds; the p-value mixture is not itself a p-value and requires explicit independent null calibration.

### Ten-year average rates across the twelve synthetic families

| Seed | Method | Null alarm | D=1 alarm | D=3 alarm |
|---|---|---:|---:|---:|
| A | Shared raw cutoff | 0.44% | 1.50% | 14.72% |
| A | Weighted null-tail mixture | 1.25% | 3.30% | 22.94% |
| A | True-family oracle (model-specific threshold; non-operational) | 3.75% | 15.44% | 52.89% |
| B | Shared raw cutoff | 1.03% | 1.94% | 20.11% |
| B | Weighted null-tail mixture | 0.53% | 1.50% | 14.03% |
| B | True-family oracle | 3.61% | 14.64% | 51.03% |

**Interpretation:** The tail mixture was more sensitive in replication A and less sensitive in B. The method's apparent gain is **not robustly replicated**, and its achieved false-alarm sizes differ from the baseline. 300 holdout paths/model are not enough for precise low-probability inference; do not claim superiority, inferiority, or robust operational 5% false-alarm control.

## Numerical instability discovered

An undertrained 100-path/model exploratory pilot yielded a clearly defective shared-raw threshold of about **9.4 million**, consistent with high-dimensional covariance overfitting/ill conditioning. This pilot was rejected. Larger attempted runs (500/1000/1000/800 and 400/700/700/500) hit execution limits **before results were produced** and are not counted. Completed runs at 260 training histories produced reasonable cutoffs but are still vulnerable to finite-sample estimation uncertainty.

## Methodological boundaries

- Purely synthetic known-onset structural declines; not a test of whether BTC has undergone an actual break.
- Model-specific true-family oracle has substantially higher realized false-alarm rate, so direct detection comparisons are not size-matched.
- Complete original v0.9 joint-distribution equivalence still awaits independent verification.
- No unknown-onset, volatility-shock, or cycle stress test for the new tail mixture in this round.
- The mixture combines marginal model-tail probabilities with history weights; formal calibration is required and was performed only for the declared twelve simulation families.

## Next

1. Improve and freeze regularized/lower-dimensional covariance score fitting before larger confirmatory runs.
2. Repeat power/AUC analysis at matched *achieved* false-alarm size with larger disjoint per-model samples.
3. Stress unknown break onset, volatility and cycle misspecification.
4. Request referee check of 12-model implementation and training-size pathology.
5. Maintain v0.9 unchanged; keep LinkedIn wording qualitative.

Full local reproducibility bundle: `bitcoin_power_law_v091_diagnostic10_2026-11-22.zip`; no licensed prices.
