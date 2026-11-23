# Referee D12–D14 response and preliminary retrospective scan (2026-11-23)

**Status: MAJOR REVISIONS / exploratory.** Source: user-supplied AI (Claude) referee report, not specialist human peer review. Published v0.9 and the frozen BTC dataset are unchanged. The complete locally generated audit, source scripts and aggregate results are in a separate licensed-price-free ZIP.

## Corrections required in our interpretation
1. **Uniform 5% size** is a worst-case across-family budget, not an average. Low average false alarms do **not** imply that available worst-case false-alarm capacity has been left unused. The binding cases are highly persistent models.
2. A large fraction of the 12 families is not well matched to the **annual daily-return volatility moments** of actual Bitcoin even if they passed v0.9's earlier residual-feature screen. Lambda-zero cases imply a ~3.7–6.1% daily SD throughout history versus observed ~2.19% in 2025. Retain as stress tests, not automatically realistic plausible noise. Claude's limited subfamily calibration shows the broad low-power conclusion persists but rates shift significantly with model selection.
3. Diagnostics 12–14 are **prospective synthetic detection** experiments, not direct empirical retrospective break tests. Avoid stating the actual 2010–2026 Bitcoin price history has been proven observationally indistinguishable from a changed underlying Power Law.
4. Label D12 model-specific **oracle-family cutoffs** rather than known-model detector. The score itself averages model features, and modest power is not a Neyman–Pearson detection bound.
5. Original/forward historical generators matched under identical noise draws to ~1.2e-14 across 12 models×3 seeds (referee's new test), stronger code-fidelity evidence than our prior marginal KS comparisons. This does not validate the family assumptions.
6. The pure Gaussian random-walk finite-information bound is **not** a bound for the actual mixed random-walk+cycle null family or Bitcoin.

## Independent 2014 data audit

I SHA-verified the frozen 5,873-row file (`ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`) and independently calculated annual daily log-return volatility:
- 2014 full-year SD **0.1133819164**.
- Excluding **2014-02-15..27** from the volatility *calculation* gives **0.0402313352**.
- Excluding five largest absolute-return days gives **0.0440889616**.
- Capping daily log-returns at +/-0.10 gives **0.0376527335**; at +/-0.15 gives **0.0442685994**.

The underlying price sequence has extremely low February 20 and 25 2014 quotes followed by ~593 on Feb 26. Historical market-wide data from independent sources show February 20 around $556 (e.g. StatMuse/OpenBitcoin); some other archived feeds exactly corroborate the frozen $111.92, consistent with dislocated, exchange-specific trading or feed choice. **Do not label this a proven transcription error or substitute a new close without provenance.** Claude's D13 sensitivity replacing just the annual sigma with .040 reduced average family-oracle CUSUM D1 10y detection 17.26%->15.81%; cross-family CUSUM 1.29%->1.18%. The prior v0.9 release is not altered.

## NEW: exploratory retrospective in-sample structural-break scan

This is the **first direct test on the actual frozen historical price observations**, addressing the referee's prospective/retrospective mismatch. Quarterly knot candidates 2013-01-01 to 2023-12-31, continuous hinge in log-age added to `ln P = alpha + B ln age + residual`, maximize incremental SSE reduction. Compare to 80 fresh no-break synthetic paths per original 12 residual models, with exact same knot search. This pilot **is not a pre-registered econometric test robust to I(0)/I(1)/fractional models**, and p-value resolution is extremely low.

- Observed best knot **2014-01-01**, residual SSE improvement **5.5188%**. Synthetic null exceedance fractions range **0.556–0.951** (all 12 models).
- Recompute after *excluding February 15–27, 2014 prices from observed and synthetic OLS scan*, retaining original simulator calibration: best knot again **2014-01-01**, SSE improvement **5.4000%**, null exceedance fractions **0.457–0.951**.
- **Interpretation:** no evidence of an unusually strong *single continuous log-age slope break* under these preliminary calibrated nulls. Not proof of an invariant true law, nor of absence of other kinds of breaks. The selected date is statistical, not causal.

## New publication status
**Major revisions, not publication-ready.** Revised paper should clearly separate descriptive Power Law fit, latent structural model and prospective detection; explicitly disclose the declared noise family, its volatility-model limitations, and the preliminary retrospective test. Until robust full-sample break tests are executed, don't make quantitative empirical claims about the past latent exponent.

**Next tasks:** fully robust retrospective break methodology with larger calibration; independently source-validate 2014 exchange quotes and decide a predeclared annual-volatility estimator; volatility-screen family members and replicate the D13 sensitivity in fresh seeds; human specialist referee if aiming for formal publication. LinkedIn may state only descriptive facts and qualified investigation, and must disclose AI-assisted review, not peer review.

Private price series, daily residuals and model-reconstructing outputs were **not** uploaded to GitHub. v0.9 remains untouched.
