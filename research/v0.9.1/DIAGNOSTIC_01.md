# v0.9.1 exploratory diagnostic 1: original frozen data
Date of computation: 2026-11-21. This is a **descriptive audit, NOT a calibrated hypothesis test**.

Input: the private frozen dataset stored in the user's file library, spanning 2010-07-17 to 2026-08-14 (5,873 complete UTC daily closes).

Integrity: input SHA-256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f` matched the published frozen hash exactly.

Procedure: log-log OLS slope with free intercept; genesis origin 2009-01-03. Month-end expanding estimates and rolling 3/5/7/10 calendar-year estimates; August 2026 endpoint is August 14 (a partial **calendar month**, but completed UTC daily close). All underlying dates/close values remain private.

## Verified numerical results
- Full sample B: **5.650938373388459** (matches published v0.9 5.6509383734).
- Expanding B, 2021-12: 5.8879514675.
- Expanding B, 2025-08: approximately 5.7027525 (computed as 2026-08 value minus the 12-month change).
- Expanding B, 2025-12: **5.698157**.
- Expanding B, 2026-08-14: **5.650938**; Aug 2025 to Aug 2026 change **−0.051814**.
- Expanding estimate fell in **10 of 12 monthly updates** through Aug 14, 2026; this is not independent-month evidence due to extreme sample overlap and persistent residuals.
- Rolling five-year B, 2025-12-31: **3.263593**.
- Rolling five-year B, 2026-08-14: **4.108164** (increase **+0.844571**).
- Rolling three-year B, 2025-12-31: 9.472108; 2026-08-14: 4.725329.
- Rolling seven-year B, 2025-12-31: 5.332940; 2026-08-14: 4.631640.
- Rolling ten-year B, 2025-12-31: 5.793415; 2026-08-14: 5.210306.

## Interpretation
The expanding estimator continued to drift lower through August 2026, but the rolling five-year estimator recovered substantially from its 2025 minimum. This divergence makes a trend break inference **premature**. v0.9 already showed how observations departing a rolling window can dominate the reported change, and constant-exponent residual models can generate similar variations.

These values are obtained **only through Aug 14, 2026** and DO NOT measure the November 2026 drawdown. A verified, separately sourced extension through completed UTC closes is needed for that analysis.

## Next stages not yet executed
1. Simultaneous null envelopes and calibrated multi-month alarm rules.
2. Independent Monte Carlo power and first-detection-lag distributions.
3. Forward real-time P10 coverage and persistent-breach tests.
4. Sensitivity to the deferred confidence-interval calibration and higher break-count caps.
5. Companion November 2026 paper comparison when available.

## Reproduction
Run `python research/v0.9.1/monthly_exponents.py /path/to/private_frozen.csv --out /tmp/monthly_summary.csv --require-frozen-hash`. Do not publish the input file or row-level outputs. The monthly aggregate CSV itself is withheld pending data-license review.
