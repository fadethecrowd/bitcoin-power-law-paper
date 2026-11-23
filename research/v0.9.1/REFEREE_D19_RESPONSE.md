# Referee D19 response — studentization, selection and all-knot coverage (2026-11-23)

**Status: major revisions. Published v0.9 unchanged.** User supplied Claude AI referee ZIP `referee_d19_2026-11-23.zip`. Referee reproduced D19 12-model calibration/holdout exactly and identified two substantive problems: fixed historical SD scaled conditional intervals valid only at D=0, and 2017/2020 knots were selected with historical-price knowledge.

## Corrected referee numbers — not cleared for publication

| Date | Original two-date fixed-scale | Corrected two-date studentized | Corrected eleven-knot simultaneous |
|---|---|---|---|
| 2017 | [-3.88,+2.83] | [-5.47,+4.45] | [-6.17,+5.11] |
| 2020 | [-5.45,+3.20] | [-6.95,+4.66] | [-7.90,+5.68] |

The corrected all-date intervals include zero and both large deterioration and substantial improvement. They apply, at best, **conditionally on the stated noise-family model, hinge specification, and coverage guarantee**; these are not universal parameters describing Bitcoin.

## Independently executed checks

- Independently verified s_full = sqrt(s_obs² − v_k * Dhat_k²) across the eleven annual dates against referee JSON, within 1e-12.
- Independently simulated 120 histories each from AR(.990)/cycle and RW/cycle families, then injected true hinge sizes D={-3,-1,0,+1,+3}. For a hinge fitted **at the actual break date**, the studentized pivot was invariant to numerical precision (~4.4e-14 AR, ~2.2e-12 RW).
- Referee holdout empirical 11-date simultaneous coverage ranges **93.75–96.35%**, while its two-date Bonferroni check ranges **95.25–96.85%**. Nominal Monte Carlo uncertainty remains; the 11-date claims need improved calibration.

## NEW challenge to referee's 11-knot *alternative* coverage claim

**Single-knot invariance is not automatically an exact all-knot post-selection pivot under arbitrary nonzero breaks.** Suppose the actual deterministic change is a 2017 hinge. At the *other* candidate knots (2014 etc.), the one-hinge regression does not fully remove the deterministic departure. Its residual SD depends on the true break size even after subtracting the appropriate projected hinge coefficient. On new synthetic paths, injecting D=±3 at 2017 changed the candidate-2014 pivot, with maximum discrepancy around 0.33 (AR .990) and 2.48 (RW mixture), while the fitted-2017 pivot did not change beyond numerical precision. This is a **mathematical counterexample to an exact joint all-knot pivot under such alternatives**, not a demonstrated 95%-coverage failure.

The referee should clarify the estimand and whether its 11-date procedure controls only the global **no-break null**, single-hinge conditional inference at the true date, or simultaneous confidence statements under arbitrary selected alternatives. Full alternative-dependent simulation coverage and correct multiple-date inversion are outstanding.

## Other corrections

D19's `holdout_coverage_joint_Dminus3` and `holdout_coverage_joint_Dplus3` were mislabeled duplicates of D=0 results; withdraw. Seed disjointness applies **within D19 only**. Same-data selection of the 12 residual families may itself be distorted by true breaks. The pure RW GLS figures are conditional theoretical benchmarks, not Bitcoin-wide bounds.

## Next gate

A licensed-price-free package `bitcoin_powerlaw_v091_d19_response_round6_2026-11-23.zip` includes the report, independent executable cross-checks, relevant original-code adapter, aggregate calibration/results, and a focused adversarial Claude review prompt. Continue only after refuting or correcting the multi-knot issue; then run end-to-end family-screening coverage and 10,000+ calibration histories/model. Do not present the D19 numeric bounds as settled publicly.
