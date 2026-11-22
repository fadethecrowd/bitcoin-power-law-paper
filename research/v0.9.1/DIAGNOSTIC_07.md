# Diagnostic 07 — Referee-corrected twelve-model structural detection and 20-year extension

**Date:** 2026-11-22. **Status: exploratory; independent Round 3 referee review pending.**

This diagnostic supersedes the *uncorrected innovation-detector* comparisons from Diagnostic 05 and the original-innovation portion of Diagnostic 06. It retains those files for audit history. **Published v0.9 and the frozen licensed dataset remain untouched.**

## Main scientific finding

A decline in the *fitted* Bitcoin Power Law exponent does not uniquely identify deterioration of the *underlying local* exponent. Simulated detectability varies substantially with residual persistence, cycle structure, conditional starting state, monitoring rule and false-alarm budget. The original 180-day EWMA was a weak monitoring method; Claude Round 2 found a missing starting-residual term in our AR-working innovation score. We corrected and reran **all twelve screened v0.9 residual models**.

### Revised ten-year comparison

4,000 synthetic null calibration paths and 2,500 independent evaluation paths per model, twelve models. Same checkpoints 1/2/5/10 years, known monitoring onset at frozen 2026-08-14 endpoint, changes D=0,0.5,1,3 (continuous log-age slope reduction).

| Actual local-exponent drop | Corrected innovation score: 2-year detection range | Corrected innovation: 10-year range | Matched 180d EWMA: 10-year range |
|---|---:|---:|---:|
| D=0 (false alarms) | 0–3.5% | 3.3–5.6% | 4.1–5.6% |
| D=0.5 | 0–4.5% | 4.4–9.7% | 5.8–8.6% |
| D=1 | 0–5.6% | 7.1–25.6% | 8.0–15.1% |
| D=3 | 0–12.6% | 23.1–99.0% | 19.6–65.5% |

**These are ranges across different stochastic models, not uncertainty intervals.** Model-specific thresholds assume the true family is known. A conservative threshold using the complete twelve-model family yielded D=1 ten-year detection only **0–8.0%** for either method; null false-alarm maximum in 2,500-path evaluation was 3.96% and 4.68%, respectively. This does not imply 5% *state-conditional* control.

### Twenty-year extension

Separate **20-year** whole-horizon calibration, also 4,000 + 2,500 independent paths/model, synthetic August 2026–August 2046. For D=1, 20-year detection was **9.0–68.4%** for corrected innovation and **9.0–24.6%** for EWMA. Specifically 68.4% for AR(.990)/cycle.8/lambda1 but only 9.0% for RW/cycle.4/lambda1. With the conservative complete-family threshold, D=1 20-year power was **0–9.0%** (corrected) and **0–9.7%** (EWMA). This is an entirely simulated future; Bitcoin does not have 20 realized post-break years of history.

### Starting state: unconditional versus conditional size

Under unconditional model-specific thresholds, certain starting states have null false-alarm rates far above nominal 5%:
- Corrected score, AR(.999)/cycle.4/lambda1, starting residual below −0.5: **70/498 = 14.1%**.
- EWMA, AR(.995)/cycle.4/lambda1, starting residual above +0.5: **79/368 = 21.5%**.

A **separate** state-conditioned 4,000-calibration/2,500-evaluation exercise/model applied order-statistic thresholds with Bonferroni-allotted 95% simultaneous confidence across 72 predeclared model × state bin × detector cells, *under iid synthetic null paths and correct model specification*. Ten-year observed null rates reduced to **1.5–5.3%** (corrected) and **1.6–5.4%** (EWMA). D=1 conditional ten-year detection was **4.3–37.3%** and **3.4–17.6%** respectively; the ranges across state/model cells are not a probability estimate for Bitcoin. Two empirical evaluation cells exceeded 5% slightly despite conservatively selected thresholds, within finite simulation uncertainty.

### Unknown-onset pilot

Three candidate monitoring starts at years 0/2/5, each with an OLS refit using only its own past history, calibrated for at least one alarm across all candidates in ten years. 600 calibration + 400 evaluation histories/model; **low-precision pilot**, *not* continuous or model-agnostic unknown-onset monitoring. True D=1 decline beginning in year 2 was detected by the end of the ten-year window in **2.5–10.2%** (corrected) or **3.0–10.0%** (EWMA) of simulations; year-5 onset D=1 only **1.5–7.0%** and **2.8–7.8%**.

### Pure random-walk theoretical observation

For a **pure Gaussian RW log-residual** with known daily innovation sigma, known onset and known deterministic trend, a permanent D decline in local log-age slope gives innovation displacement proportional to **D/(age+t)**. Its squared Gaussian signal-to-noise is the sum of approximately **1/(age+t)^2**, hence converges even as monitoring time goes to infinity. At age 6,432, sigma=0.0219/day, D=1, one-sided 5% fixed-horizon test, the idealized power ceiling is about **14.1% at infinite horizon**, versus 9.6% after 10 years. The theorem is **not** a numeric ceiling for Bitcoin or the original mixed RW+stochastic-cycle/declining-volatility model. Its proof and applicability require external referee review.

## Reproducibility and constraints

- Private frozen 5,873-row CSV SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f` checked; fitted B=5.6509383734.
- 33 local tests passed; a new exact-reproduction rerun of the fractional model recovered identical cutoffs and every ten-year rate.
- Future volatility mean-of-2023–25 versus 2025-only sensitivity: D=1 ten-year power differed by at most 1.0 percentage point (corrected) and 0.63 points (EWMA) in lower-precision matched-seed trials.
- The complete code/results, 19 kB consolidated report and Claude Round 3 adversarial review brief are in the user's **2026-11-22 consolidated referee ZIP**; the archive intentionally contains **no licensed BTC prices**.
- Other limitations: pinned v0.9 environment not completely rerun; complete null **joint-distribution** equality pending; ideal/model-specific assumptions; arbitrary starting-state cutpoints; unknown true residual model; only a three-start scanning pilot; untested alternative structural-break definitions; no evidence of an actual current Bitcoin true-exponent change.

## Proposed paper claims

1. Strong retrospective scaling does not imply a dependable real-time structural-break alarm.
2. A fitted exponent decline may arise from persistent departures from unchanged trend.
3. Detection power is highly model-, method-, state- and horizon-dependent; no universal 2-year or 10-year power bound can be inferred from our experiments.
4. A pure Gaussian RW noise **model**, under explicitly fixed hypotheses, admits a finite-information property for a permanent local-exponent step; external mathematical checking is required before paper-level use.

**Next review gate:** send consolidated Round 3 ZIP to Claude; request adversarial scrutiny of order-statistic calibration, 12-model equivalence, starting-state whitening, unknown-onset implementation, and theoretical finite-information proof. Only after response should we revise the paper's conclusions and publish quantitative LinkedIn claims.
