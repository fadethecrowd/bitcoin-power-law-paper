# Referee Round 2 — Assessment (2026-11-22)

**Source:** user-supplied `referee_round2_2026-11-22.zip` (README, `round2.json`, `round2_checks.py`, `multiplicity_and_bound.py`, text output). Inspected entire referee script/methodology and supplied aggregate results. Independently re-ran the supplied multiplicity/theoretical-bound script and created the corrected-score code with 5 passing tests. **Did not independently rerun all original referee simulations.** Referee's direct replication covers **five lambda=0 models, not all twelve**. Original reproduction relies on earlier code and a referee-machine hardcoded path.

## Key result: innovation-monitor mathematical correction

The historical-vintage anchored forecast gap is `gap_t = r_t-r_0`. The previous detector computed `gap_t-rho*gap_(t-1)`, which incorrectly treats the observed starting residual `r_0` as zero. Correct working AR innovation:

`r_t-rho*r_(t-1) = [gap_t-rho*gap_(t-1)] + (1-rho)*r_0`.

Implemented `state_corrected_score.py` and `test_state_corrected_score.py`. Five local tests passed: direct residual-level equivalence, zero-start agreement with old method, sensitivity to starting state, no future-to-past influence, sign of starting state. This remains only an AR(.997) working score and is **not** a correct likelihood for arbitrary cycle, fractional or RW processes.

### Ten-year referee results, D=1 and D=3, 5 lambda=0 models

| AR rho | D1 old | D1 corrected | D3 old | D3 corrected |
|---|---:|---:|---:|---:|
| .990 | 9.2% | 8.7% | 30.0% | 71.7% |
| .995 | 10.5% | 11.6% | 30.7% | 60.1% |
| .997 | 9.8% | 10.1% | 28.5% | 47.1% |
| .998 | 8.5% | 10.5% | 24.4% | 39.6% |
| .999 | 7.6% | 6.6% | 19.9% | 22.3% |

Referee employed fresh 6,000 calibration and 4,000 evaluation paths/model for its corrected-score comparisons. The D1 effects are mixed; D3 power often improves dramatically. Old innovation-score power should **not** be presented as a well-specified benchmark.

Null final-score correlation with starting residual r0 fell from 0.54–0.86 to -0.24–0.29 after correction, but this is **not** proof of state-conditional size control. Referee's near-current-start r0=-0.78±0.15 subset had 363–406 evaluation histories/model, insufficient for precise 5% conditional rates; this subset was chosen with awareness of observed Bitcoin positioning.

## Multiplicity and false alarms

Across 72 conditional cells (12 models × 3 starting bins × 2 monitors), 10 had evaluation false-alarm rates above 5%, with max 45/568 = 7.92%. Single-cell one-sided p=0.002, Bonferroni ×72 ≈0.13. Multiple testing and sample uncertainty mean **no convincing joint evidence of systematic miscalibration**, but this is not positive proof that all individual false-alarm probabilities are <=5%. Referee's illustrative 72 independent-binomial simulation is **not an exact joint significance test** for the dependent empirical cells. Pooled null rate 3.75% is not a conditional or worst-family guarantee.

## Pure-random-walk information ceiling (mathematical contribution)

For a **pure Gaussian random-walk log residual** with fixed, known innovation sigma, trend and onset, after local exponent declines by D the daily innovation mean shift is `-D log((age+t)/(age+t-1))`. Its fixed-horizon optimal Gaussian separation obeys:

`SNR_H²=(D²/sigma²) sum[t=1..H] log((age+t)/(age+t-1))²`.

Because the terms decay approximately as `1/(age+t)²`, the sum converges for H → infinity: **even observing indefinitely gives finite total information** for this specific step-down alternative. At age 6432 days, sigma=0.0219/day, D=1 and 5% one-sided size, referee's figures are ~9.6% ideal power by 10 years and ~14% in the asymptotic limit. Re-ran the referee's script independently and reproduced its printed values.

**Very narrow interpretation:** This ceiling holds for a *specific simple Gaussian RW experiment*, with its fixed sigma and ideal known parameters; it does **not** establish a universal bound for Bitcoin, for the original screened `rw|cyc0.4|lam1` mixture, for data-driven parameter uncertainty, or for every definition of a structural break. It is an important mathematical lead for the paper, conditional on explicit assumptions, not an empirical Bitcoin conclusion.

## Review status and next steps

1. Round 2 materially **corrected** the innovation score and strengthened caution about deriving any universal detection impossibility from EWMA weakness. 
2. Test corrected monitor on all 12 families, with predeclared false-alarm budget and independent evaluation; retain old results only as historical diagnostics.
3. Study unknown onset and unknown model: existing protocols are largely *known monitoring-start* experiments.
4. Validate conditional thresholds with adequately sized strata / simultaneous uncertainty.
5. Extend 20-year tests and scrutinize pure-RW mathematical bound versus original mixed RW+cycle family.
6. Request final independent challenge to the full-family implementation before definitive claims; public LinkedIn post should emphasize the research question and qualified model-dependence.

Published v0.9 and retirement dashboard are untouched. Supporting local runnable assessment bundle: `bitcoin_powerlaw_v091_referee_round2_assessment_2026-11-22.zip` (not committed to repo; public repository contains reviewed code/tests).
