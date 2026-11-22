# Diagnostic 08 — Matched nominal size and threshold-free ROC audit (2026-11-22)

**Status:** exploratory 12-family synthetic replication; published v0.9 is frozen. A full licensed-price-free reproduction package and report were generated in the active research session.

## Why this experiment was required

The previous 12-family adaptive detectors were calibrated to about **0.69% / 0.65%** observed average false-alarm size; the true-family comparator was calibrated near **3.67%**. A comparison of their raw detection percentages therefore confounded **score discrimination** with **threshold conservatism**. This audit compares per-family nominally matched false-alarm rates of 1%, 2%, 5%, and 10%, plus 10-year **AUC**, which is independent of the choice of alarm cutoff.

## Protocol

For each of the twelve v0.9-screened models, use **300 training, 400 independent calibration, 300 independent evaluation** paths (12,000 synthetic histories total). The frozen private Bitcoin CSV was verified against SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`; no prices distributed. Alternative D=1 local log-age exponent decline begins at the known 2026-08-14 endpoint, uses the same simulated random shocks as null; scores observed at 1,2,5,10 years. Compare historical-feature posterior-weighted, history-selected model and an **oracle true-family identity** comparator; none uses a known true latent exponent. Training, calibration and holdout use disjoint seeds.

The per-model 95th-percentile calibration used here is intentionally **not** a simultaneous familywide 5% confidence bound, and requires knowledge of the generating family for model-specific threshold selection. 300-path evaluation cannot precisely measure individual-cell size in the 1–5% tails.

## 10-year discrimination (D=1 versus D=0)

| Method | Mean AUC over 12 families | Model AUC range | Mean null size at nominal 5% | Mean D1 detection at nominal 5% |
|---|---:|---:|---:|---:|
| Posterior-weighted | 0.677 | 0.574–0.914 | 5.03% | 18.25% |
| History-selected | 0.657 | 0.556–0.899 | 4.89% | 16.19% |
| True-family identity oracle | 0.679 | 0.568–0.938 | 5.56% | 20.03% |

AUC was calculated on *held-out* D0 and D1 maximum checkpoint scores. Cross-pair ranking makes AUC cutoff-independent, although simulated data/model assumptions still apply. The similarity of descriptive **mean AUC** for posterior-weighting (0.677) and oracle identity (0.679) indicates the previous dramatic low-power gap **cannot be attributed entirely to poor adaptive score discrimination**. Model-specific differences remain important; this is not an inferential equivalence claim.

Mean D1 rates at **nominal** operating points 1% / 2% / 5% / 10%:
- Weighted: **7.00 / 10.39 / 18.25 / 28.67%**.
- Selected: **6.44 / 9.58 / 16.19 / 25.83%**.
- Oracle identity: **7.94 / 11.58 / 20.03 / 30.11%**.

Observed false-alarm sizes approximate but do **not** exactly equal the targets in every model; achieved-size matching is still imperfect.

## Familywide false-alarm control remains unresolved

Applying the *maximum across twelve empirical 95th-percentile cutoffs* yielded mean null alarms 2.03% weighted / 2.53% selected, but **worst-family holdout alarms 6.33% / 8.00%**, respectively. A naive shared empirical cutoff therefore **fails to demonstrate** worst-family <=5% whole-path control. Prior Bonferroni/upper-confidence cutoffs were more conservative and consequently less powerful. A practical detector requires robust **uniform** size calibration, not just model-specific ROC quality.

## Changing future volatility

Independent evaluation paths with completed-2023–25 mean future volatility instead of completed-2025 volatility, holding training and calibration unchanged, produced mean AUCs:
- Weighted **0.672** (baseline 0.677)
- Selected **0.652** (baseline 0.657)
- Oracle **0.673** (baseline 0.679)

Only lambda=1 families respond to this perturbation. This is a limited sensitivity check, not coverage of volatility shocks or changing cycles.

## Research interpretation

A strong historic Power Law fit, a stable latent scaling law, and prospectively identifying structural deterioration are separate claims. The fresh evidence suggests **two distinct obstacles** for adaptive detection: underlying score discrimination *and*, separately, obtaining sufficiently robust cross-family thresholds at a tolerable false-alarm budget. The former need not always be terrible in these simulations; the latter remains an important unresolved barrier.

This does not establish that Bitcoin's underlying exponent has changed, that the Power Law is permanent, or that real-time detection is universally impossible.

## Execution / next steps

- **Completed now:** ROC/AUC and per-model nominal size–power audit across all 12, future-volatility sensitivity, reproducibility package and independent exact script rerun (same aggregated output).
- **Not completed:** high-precision simultaneous calibration across 12 models and conditional initial states, continuous unknown-onset monitoring, out-of-family stress tests, independent referee approval.
- Next: larger calibration/holdout with robust cross-family simultaneous coverage; practical unknown-onset detector; adversarial referee review of AUC and model-specific versus robust-size distinction.

Keep the public v0.9 and retirement dashboard unchanged.
