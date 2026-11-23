# Diagnostics 16–18 — Two historical slope breaks and persistence sensitivity (2026-11-23)

**Exploratory / independent Claude referee review pending. Published v0.9 is frozen. Private daily prices and historical residuals are NOT uploaded here.**

The next retrospective tests evaluate a one- or two-hinge extension of the frozen 2010–2026 log-price-versus-log-age fit. Eleven annual knot candidates 2013–2023, two hinges at least two years apart; the maximum SSE reduction is recalculated for each generated no-break null history to account for selecting the most favorable break dates.

## Findings

- Original single-hinge best 2014-01-01, improvement **5.5188% of residual SSE**.
- Best two-hinge pair **2014-01-01 and 2016-01-01**, combined improvement **12.4720% of original residual SSE**. This is *not* 12.47% of total price variance.
- Under **500 newly simulated histories per original screened residual family** (12 families), same-selection two-hinge empirical no-break exceedance probabilities **0.561–0.986**. A distinct **1,000 histories/family** check gave **0.540–0.982**. No tested family treats this double-hinge improvement as extraordinary.
- A stylized alternative where log-age local exponent falls by **1** in 2017 and rises by **0.5** in 2021 (net -0.5) was detected with model-specific 95th-null-percentile cutoffs in **3.2–9.6%** of 250 independent evaluation histories per model. This weak power makes absence of a detected break weak affirmative evidence of stability.
- Excluding **2014-02-15 through 2014-02-27** from both observed and simulated regression fit rows (while retaining frozen generator volatility calibration) changes the best two-hinge SSE improvement from **12.4720% to 12.3074%**, with the same knots and null p range **0.548–0.983**. This is only a limited price-row exclusion sensitivity, not complete volatility-data repair.
- Out-of-family circular moving-block resampling of detrended observed residuals showed **extreme dependence on assumed memory length**. With 2,000 paths/block length, p-values for blocks 30/60/90/120/180/240/365/540/730 days were **0.00050/0.00750/0.04998/0.11594/0.27486/0.40880/0.51574/0.56372/0.52624**, respectively. An independently seeded 3,000-path spot check reproduced the broad contrast.

**CRITICAL:** Circular block bootstrap is not established as valid for near-I(1), fractional, cyclic or heterogeneous-variance residuals. Short blocks mechanically remove long persistence. **The low p-values at 30–90 days do not establish a real Bitcoin structural break.** The experiment is a sensitivity demonstration only.

## Validation and next gate

Five local tests passed; direct Gram-inverse vs full two-hinge OLS SSE formula matches to numerical precision. This research's complete portable source, aggregate JSON and adversarial referee brief are in the user's ZIP `bitcoin_powerlaw_v091_d16_d18_claude_referee_2026-11-23.zip`. The source scripts require the SHA-pinned private historical BTC CSV to reproduce the original-data aggregates; the ZIP intentionally excludes it.

The defensible current interpretation is that **a strong historical descriptive Power Law fit**, **a genuine latent structural exponent**, and **prospective identifiability of a change** remain distinct scientific propositions. These tests do not prove either structural constancy or structural breakdown.

**Next user handoff:** provide the packaged ZIP and adversarial brief to Claude for critique; implement only the empirically/statistically justified corrections after feedback. Maintain published v0.9 and retirement dashboard unchanged.
