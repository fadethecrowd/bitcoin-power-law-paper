# Diagnostic 15 — Retrospective structural-break and sensitivity/power audit (2026-11-23)

**Status:** exploratory, awaiting independent referee. Frozen published v0.9 and licensed 5,873-row source dataset unchanged. A full reproducibility package with scripts and *aggregate-only* outputs was produced in the conversation.

## Historical search: same-selection Monte Carlo null calibration

Real frozen 2010-07-17–2026-08-14 log-BTC-price vs log-age OLS is fit with an unknown continuous **single slope kink**, scanning quarterly knots. Statistic is maximum fractional OLS residual SSE removed; for each null synthetic path, the entire knot search is repeated. **1,500 independent null paths per model** across the original 12 screened v0.9 persistence+cycle/volatility processes.

| Search and observed data | Best knot | Residual SSE removed | Null p-value range, 12 families |
|---|---|---:|---:|
| 2013–23, full prices | 2014-01-01 | 5.519% | 0.529–0.942 |
| 2017–23, full prices | 2021-07-01 | 4.366% | 0.261–0.879 |
| 2013–23, exclude 2014-02-15..27 in regression | 2014-01-01 | 5.400% | 0.540–0.944 |
| 2017–23, exclude same interval | 2021-07-01 | 4.369% | 0.261–0.879 |

2014 annual return-SD sensitivity: hold frozen prices fixed, replace **only 2014 synthetic annual volatility parameter** 0.1133819164 with 0.0402313352; **800 null paths/model** return p-values 0.522–0.958 for broad single-kink scan. Source quote provenance remains unresolved; no price repairs made.

## Different-class *gradual* exponent-break search

Search 72 templates for local log-age exponent linearly declining over **2 or 4 calendar years**, onset quarterly 2013–21, and staying lower afterward. Same-template-selection null calibration: **900 null paths/model**. Best observed template: **2-year decline starting 2013-01-01**, an **edge-of-search date**, removing **4.662%** of original residual SSE. Per-model null p-value range **0.391–0.937**. No template is unusually significant under the specified noise generators. An edge-optimal knot does not establish an event in 2013.

## CRITICAL: low retrospective statistical power

**Independent 800 evaluation paths/model**, with D units true immediate local exponent decline and model-specific 95th-percentile maximum-kink null cutoff. Across twelve models, mean detection rates:

| True D | Onset 2017 | Onset mid-2021 |
|---:|---:|---:|
| 0.5 | 6.6% | 5.5% |
| 1 | **10.9%** | **6.3%** |
| 2 | 29.3% | 10.2% |
| 3 | 54.8% | 16.9% |

Gradual-template sensitivity check: **300 evaluation paths/model** and model-specific 95th-percentile max-ramp cutoff. True D=1, gradual local slope ramps: 2-year onset 2017 **11.0%**; 4-year onset 2017 **9.7%**; 2-year onset mid-2021 **6.1%**; 4-year onset mid-2021 **5.5%**.

**Interpretation:** Although the actual historical series is not unusually improved by a searched single kink or gradual 2/4-year local-slope ramp under the twelve declared models, these tests generally have very poor ability to detect moderate true historical exponent deterioration. **DO NOT interpret non-rejection as confirmation of structural stability.**

## Constraints

The inference is conditional on synthetic residual families screened using the same full historical data and calibrated to historical detrended residual variance and annual volatility; the tests are retrospective and exploratory, not distribution-free, not a pre-registered independent data holdout, and are not proof of a latent law. Model-specific thresholds assume true noise family identity. Tests do not cover multiple breaks, intercept discontinuities, jumps, broader time-varying trends, or model misspecification. Source-v09 environment and external specialist peer review remain open.

## Next execution

Review the complete reproducibility package independently, then stress against out-of-family processes and alternative multi-break structures. If aiming to publish v0.9.1, state both the high per-family non-rejection *and* the poor test power prominently, and do not change public v0.9.
