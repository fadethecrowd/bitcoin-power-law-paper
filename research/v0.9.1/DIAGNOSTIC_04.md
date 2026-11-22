# v0.9.1 Diagnostic 04 — detector comparison and gradual-change sensitivity

**Date:** 2026-11-22. **Status:** exploratory full-family simulation, NOT a demonstrated Bitcoin structural break or a universal impossibility of detection. Complete reproduction scripts, aggregate data and referee brief are bundled separately; no licensed price series committed.

## Historical generator fidelity
The original frozen 5,873-row BTC sample was verified against published SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`. The generator used the original twelve screened AR/cycle, fractional/cycle and RW/cycle null processes, the original historical annual volatility profile, the original free-intercept OLS fit and simulated historical-only detrended residual SD scaling; no future observed prices or future simulated residuals were used to normalize the historical scale.

Across **600 new simulations/model**, compared to original v0.9 `screening.csv` medians, maximum absolute median differences across 12 models were: ACF(1) **0.0002**, ACF(365) **0.0181**, ACF(1461) **0.0161**, zero crossings **6**, amplitude ratio **0.0453**, daily-volatility ratio **0.0037**, 3–5y spectral share **0.0137**, skew **0.0329**. This is an engineering median check, **not** full distributional equivalence.

## Detector experiment
- Three downside EWMA detectors of future log-price deviations from the **pre-change, historically fitted** Power Law, anchored to last historical residual: half-lives **90/180/365 days**. Candidate combined daily minimum across all three windows gave numerically identical first-alarm behaviour to EWMA90 in this simulation, so was not an independent gain.
- A true abrupt local-exponent drop D gives a **continuous** log-price trend displacement `-D*ln((age+days)/age)`. Scenarios D={0,0.5,1,3}. Alternative paths reuse the same noise draws as D=0.
- Twelve null models × **5,000 null calibration paths** and **3,000 disjoint evaluation paths**. Ten-year whole-path false-alarm threshold for each model/monitor, and most conservative common threshold across 12 models.
- To reduce calibration sampling risk, model cutoffs used the **225th of 5,000 ordered null-path minima**, an upper one-sided 95% *marginal* binomial calibration at alpha 5%; not a joint 95% family guarantee.

### D=1.0 detection probability across the 12 models
| Detector | 2-year with model-specific cutoff | 10-year with model-specific cutoff | 10-year with conservative common cutoff |
|---|---|---|---|
| 90-day | 0.07–3.17% | 6.67–12.93% | 0–8.63% |
| 180-day | 0.03–2.27% | 6.57–13.87% | 0–8.53% |
| 365-day | 0–0.93% | 6.80–15.53% | 0–8.97% |

For D=3, the 10-year model-specific power rose to 18.57–58.27% (90d), 19.63–63.33% (180d) and 20.90–68.47% (365d). The model-specific rates rely on an oracle knowledge of which residual family applies; conservative cross-family rates are much lower for most models. **Do not equate any of these rates with Bitcoin's actual break probability.**

### Size validation
With D=0, independent 3,000-path per-model ten-year false-alarm rates ranged approximately 3.67–5.73% across the three rules. The binding model `ar0.999|cyc0.4|lam0` exceeded the 5% target in the smaller evaluation set. A **new independent 10,000-path holdout on that same model with previously frozen cutoffs** found:
- 90d: **478/10,000 = 4.78%**, exact two-sided 95% CI **4.37–5.22%**;
- 180d: **4.62%**, CI **4.22–5.05%**;
- 365d: **4.66%**, CI **4.26–5.09%**.

This is broadly consistent with ~5% target but **not** proof that every method/model combination is controlled below 5%, because even the larger intervals include greater values and marginal calibration is not simultaneous across all models and tests.

### Two-year gradual local-exponent decline
A separate **3,000 paired evaluation paths/model**, using the same thresholds, made local exponent decline linearly in log-age over the first two years and then remain lower by D. For 180-day EWMA, ten-year model-specific detection:
- D=0.5: **4.5–7.7%** (abrupt **4.9–8.4%**)
- D=1.0: **5.8–11.5%** (abrupt **6.6–13.9%**)
- D=3.0: **16.4–50.7%** (abrupt **19.6–63.3%**)

Across this tested family and EWMA detectors, a gradual change is harder to identify than an abrupt break of the same eventual exponent size.

## Interpretation
**Supported narrowly:** Under the originally screened persistent residual processes and these three EWMA forecast-gap monitors, substantial true local-exponent deterioration is very difficult to detect within 2 years without an elevated ten-year false-alarm budget; longer smoothing can improve ten-year performance but not early warning. This is **not proof** the Bitcoin Power Law is broken, that its exponent truly declined, or that more efficient detectors cannot do much better.

## Remaining mandatory gates
1. **Adversarial statistical referee review**, including whether pre-onset per-path historical normalization biases detection difficulty and whether the twelve selected models omit important alternatives.
2. Compare a **different class** of detector (likelihood-based, CUSUM of innovations, composite change-point or rolling fitted slope) with matched error budgets; multiple EWMA windows alone are not an adequate competition.
3. True 20-year horizon/resolution curves with a *20-year* 5% whole-path false-alarm threshold; uncertainty accounting for family/model selection.
4. Pin/reproduce environments and publish runnable new scripts before presenting v0.9.1 findings as definitive. Published v0.9 remains unchanged.

**Public communication:** It is defensible to post about the *research question* and preliminary detector-specific limitation, but not to assert early detection is fundamentally impossible or the Power Law is invalid.
